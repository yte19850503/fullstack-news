from __future__ import annotations

import re
import time

from sqlalchemy import or_, text as sa_text
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.article import Article, ArticleTag, ArticleStatus
from app.core.exceptions import AppError
from app.core.sanitizer import sanitize_text, sanitize_html
from app.services.cache import cache_service
from app.services.view_counter import view_counter
from app.services.cache import redis_client

HOT_TERMS_KEY = "search:hot_terms"
HOT_TERMS_SIZE = 20


def _to_slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fa5]+", "-", title.lower()).strip("-")
    return f"{slug}-{int(time.time() * 1000):x}"


class ArticleService:
    def list(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        category_id: int | None = None,
        status: str | None = None,
        q: str | None = None,
        tag_id: int | None = None,
        author_id: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        sort: str = "newest",
    ) -> dict:
        cache_key = (
            f"article:list:{category_id}:{status}:{q}:{tag_id}:{author_id}"
            f":{date_from}:{date_to}:{sort}:{page}:{page_size}"
        )
        cached = cache_service.get(cache_key)
        if cached:
            return cached

        query = db.query(Article).options(
            joinedload(Article.author),
            joinedload(Article.category),
            joinedload(Article.tags).joinedload(ArticleTag.tag),
        )

        query = self._apply_filters(db, query, category_id, status, q, tag_id, author_id, date_from, date_to)
        query = self._apply_sort(query, sort)

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        seen = set()
        unique_items = []
        for item in items:
            if item.id not in seen:
                seen.add(item.id)
                unique_items.append(item)

        result = {
            "items": [self._to_brief(a) for a in unique_items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
        cache_service.set(cache_key, result, ttl=300)
        return result

    def _apply_filters(
        self,
        db: Session,
        query,
        category_id: int | None,
        status: str | None,
        q: str | None,
        tag_id: int | None,
        author_id: int | None,
        date_from: str | None,
        date_to: str | None,
    ):
        if category_id:
            query = query.filter(Article.category_id == category_id)
        if status:
            query = query.filter(Article.status == status)
        if author_id:
            query = query.filter(Article.author_id == author_id)

        if q:
            like_pattern = f"%{q}%"
            query = query.filter(
                or_(
                    Article.title.like(like_pattern),
                    Article.summary.like(like_pattern),
                    Article.content.like(like_pattern),
                )
            )

        if tag_id:
            query = query.join(ArticleTag).filter(ArticleTag.tag_id == tag_id)

        if date_from:
            query = query.filter(Article.created_at >= date_from)
        if date_to:
            query = query.filter(Article.created_at <= f"{date_to} 23:59:59")

        return query

    def _apply_sort(self, query, sort: str):
        if sort == "popular":
            return query.order_by(Article.view_count.desc(), Article.created_at.desc())
        return query.order_by(Article.created_at.desc())

    def search_fulltext(self, db: Session, q: str, page: int = 1, page_size: int = 20) -> dict:
        cache_key = f"article:fulltext:{q}:{page}:{page_size}"
        cached = cache_service.get(cache_key)
        if cached:
            self.track_search_term(q)
            return cached

        match_sql = sa_text("MATCH(title, content) AGAINST(:q IN BOOLEAN MODE)")

        count_q = db.query(Article).filter(match_sql.bindparams(q=q))
        total = count_q.count()

        items = (
            db.query(Article)
            .options(
                selectinload(Article.author),
                selectinload(Article.category),
                selectinload(Article.tags).selectinload(ArticleTag.tag),
            )
            .filter(match_sql.bindparams(q=q))
            .order_by(sa_text("MATCH(title, content) AGAINST(:q IN BOOLEAN MODE) DESC").bindparams(q=q))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        unique_items = []
        seen = set()
        for article in items:
            if article.id not in seen:
                seen.add(article.id)
                unique_items.append(article)

        self.track_search_term(q)

        result = {
            "items": [self._to_brief(a) for a in unique_items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "search_mode": "fulltext",
        }
        cache_service.set(cache_key, result, ttl=300)
        return result

    def track_search_term(self, term: str) -> None:
        term = term.strip().lower()[:100]
        if not term:
            return
        redis_client.zincrby(HOT_TERMS_KEY, 1, term)

    def get_hot_search_terms(self, top: int = 10) -> list[dict]:
        cached = cache_service.get("search:hot_terms_result")
        if cached:
            return cached

        results = redis_client.zrevrange(HOT_TERMS_KEY, 0, top - 1, withscores=True)
        terms = [
            {"term": term.decode() if isinstance(term, bytes) else term, "count": int(score)} for term, score in results
        ]
        cache_service.set("search:hot_terms_result", terms, ttl=60)
        return terms

    def get_by_slug(self, db: Session, slug: str) -> dict:
        cache_key = f"article:detail:{slug}"
        cached = cache_service.get(cache_key)
        if cached:
            view_counter.increment(cached["id"])
            return cached

        article = (
            db.query(Article)
            .options(
                joinedload(Article.author),
                joinedload(Article.category),
                joinedload(Article.tags).joinedload(ArticleTag.tag),
            )
            .filter(Article.slug == slug)
            .first()
        )
        if not article:
            raise AppError("Article not found", 404)

        view_counter.increment(article.id)
        result = self._to_detail(article)
        cache_service.set(cache_key, result, ttl=600)
        return result

    def create(self, db: Session, data: dict, author_id: int) -> dict:
        title = sanitize_text(data["title"]) or data["title"]
        content = sanitize_html(data["content"]) or data["content"]
        summary = sanitize_text(data.get("summary")) if data.get("summary") else None

        slug = _to_slug(title)
        article = Article(
            title=title,
            slug=slug,
            content=content,
            summary=summary,
            cover_image=data.get("cover_image"),
            status=data.get("status", ArticleStatus.DRAFT),
            author_id=author_id,
            category_id=data["category_id"],
        )
        db.add(article)
        db.flush()

        for tag_id in data.get("tag_ids") or []:
            db.add(ArticleTag(article_id=article.id, tag_id=tag_id))

        db.commit()
        db.refresh(article)

        cache_service.delete_by_pattern("article:list:*")
        return self._to_detail(article)

    def update(self, db: Session, article_id: int, data: dict) -> dict:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise AppError("Article not found", 404)

        for field in ("cover_image", "category_id", "status"):
            if field in data and data[field] is not None:
                setattr(article, field, data[field])

        if "title" in data and data["title"] is not None:
            article.title = sanitize_text(data["title"]) or data["title"]
        if "content" in data and data["content"] is not None:
            article.content = sanitize_html(data["content"]) or data["content"]
        if "summary" in data and data["summary"] is not None:
            article.summary = sanitize_text(data["summary"])

        if "tag_ids" in data and data["tag_ids"] is not None:
            db.query(ArticleTag).filter(ArticleTag.article_id == article_id).delete()
            for tag_id in data["tag_ids"]:
                db.add(ArticleTag(article_id=article_id, tag_id=tag_id))

        db.commit()
        db.refresh(article)

        cache_service.delete(f"article:detail:{article.slug}")
        cache_service.delete_by_pattern("article:list:*")
        return self._to_detail(article)

    def delete(self, db: Session, article_id: int) -> None:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise AppError("Article not found", 404)

        cache_service.delete(f"article:detail:{article.slug}")
        db.delete(article)
        db.commit()
        cache_service.delete_by_pattern("article:list:*")

    def _to_brief(self, article: Article) -> dict:
        return {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "summary": article.summary,
            "cover_image": article.cover_image,
            "status": article.status.value if article.status else "DRAFT",
            "view_count": article.view_count,
            "created_at": article.created_at.isoformat() if article.created_at else None,
            "updated_at": article.updated_at.isoformat() if article.updated_at else None,
            "author": {
                "id": article.author.id,
                "name": article.author.name,
                "avatar": article.author.avatar,
            }
            if article.author
            else None,
            "category": {
                "id": article.category.id,
                "name": article.category.name,
                "slug": article.category.slug,
            }
            if article.category
            else None,
            "tags": [{"id": at.tag.id, "name": at.tag.name, "slug": at.tag.slug} for at in article.tags if at.tag],
        }

    def _to_detail(self, article: Article) -> dict:
        data = self._to_brief(article)
        data["content"] = article.content
        return data
