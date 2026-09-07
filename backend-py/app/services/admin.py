from __future__ import annotations

from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.article import Article
from app.models.category import Category
from app.models.tag import Tag
from app.models.comment import Comment
from app.models.operation_log import OperationLog
from app.core.exceptions import AppError


class AdminService:
    # ── 用户管理 ──────────────────────────────────────────

    def list_users(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        role: str | None = None,
        q: str | None = None,
    ) -> dict:
        query = db.query(User)
        if role:
            query = query.filter(User.role == role)
        if q:
            like = f"%{q}%"
            query = query.filter(User.name.like(like) | User.email.like(like))
        total = query.count()
        items = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return {
            "items": [self._user_to_dict(u) for u in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def update_user(self, db: Session, user_id: int, data: dict, operator_id: int) -> dict:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AppError("User not found", 404)

        changes = []
        if "name" in data and data["name"] is not None:
            user.name = data["name"]
            changes.append(f"name -> {data['name']}")
        if "role" in data and data["role"] is not None:
            old_role = user.role.value
            user.role = data["role"]
            changes.append(
                f"role: {old_role} -> {data['role'].value if hasattr(data['role'], 'value') else data['role']}"
            )

        db.commit()
        db.refresh(user)

        if changes:
            self.log(db, operator_id, "update_user", "user", user_id, "; ".join(changes))
        return self._user_to_dict(user)

    def toggle_user_active(self, db: Session, user_id: int, is_active: bool, operator_id: int) -> dict:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AppError("User not found", 404)

        user.is_active = is_active
        db.commit()
        db.refresh(user)

        self.log(db, operator_id, "toggle_active", "user", user_id, f"is_active -> {is_active}")
        return self._user_to_dict(user)

    # ── 文章管理 ──────────────────────────────────────────

    def list_articles(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        q: str | None = None,
    ) -> dict:
        query = db.query(Article).options(
            joinedload(Article.author),
            joinedload(Article.category),
        )
        if status:
            query = query.filter(Article.status == status)
        if q:
            like = f"%{q}%"
            query = query.filter(Article.title.like(like))

        total = query.count()
        items = query.order_by(Article.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        seen = set()
        result = []
        for a in items:
            if a.id not in seen:
                seen.add(a.id)
                result.append(self._article_to_dict(a))
        return {
            "items": result,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def review_article(self, db: Session, article_id: int, status: str, operator_id: int) -> dict:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise AppError("Article not found", 404)

        old_status = article.status.value
        article.status = status
        db.commit()
        db.refresh(article)

        self.log(db, operator_id, "review_article", "article", article_id, f"status: {old_status} -> {status}")
        return self._article_to_dict(article)

    def batch_update_articles(self, db: Session, article_ids: list[int], status: str, operator_id: int) -> dict:
        updated = 0
        for aid in article_ids:
            article = db.query(Article).filter(Article.id == aid).first()
            if article:
                article.status = status
                updated += 1
        db.commit()

        self.log(db, operator_id, "batch_update", "article", None, f"ids={article_ids}, status -> {status}")
        return {"updated": updated, "status": status}

    # ── 分类管理 ──────────────────────────────────────────

    def list_categories(self, db: Session) -> list[dict]:
        cats = db.query(Category).order_by(Category.id).all()
        return [{"id": c.id, "name": c.name, "slug": c.slug, "description": c.description} for c in cats]

    def create_category(self, db: Session, name: str, description: str | None, operator_id: int) -> dict:
        import re

        slug = re.sub(r"[^a-z0-9\u4e00-\u9fa5]+", "-", name.lower()).strip("-")
        cat = Category(name=name, slug=slug, description=description)
        db.add(cat)
        db.commit()
        db.refresh(cat)
        self.log(db, operator_id, "create_category", "category", cat.id, f"name={name}")
        return {"id": cat.id, "name": cat.name, "slug": cat.slug, "description": cat.description}

    def update_category(
        self, db: Session, category_id: int, name: str | None, description: str | None, operator_id: int
    ) -> dict:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            raise AppError("Category not found", 404)
        if name is not None:
            cat.name = name
        if description is not None:
            cat.description = description
        db.commit()
        db.refresh(cat)
        self.log(db, operator_id, "update_category", "category", category_id, f"name={name}")
        return {"id": cat.id, "name": cat.name, "slug": cat.slug, "description": cat.description}

    def delete_category(self, db: Session, category_id: int, operator_id: int) -> None:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            raise AppError("Category not found", 404)
        db.delete(cat)
        db.commit()
        self.log(db, operator_id, "delete_category", "category", category_id, f"name={cat.name}")

    # ── 标签管理 ──────────────────────────────────────────

    def list_tags(self, db: Session) -> list[dict]:
        tags = db.query(Tag).order_by(Tag.id).all()
        return [{"id": t.id, "name": t.name, "slug": t.slug} for t in tags]

    def create_tag(self, db: Session, name: str, slug: str, operator_id: int) -> dict:
        existing = db.query(Tag).filter(Tag.slug == slug).first()
        if existing:
            raise AppError("Tag slug already exists", 400)
        tag = Tag(name=name, slug=slug)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        self.log(db, operator_id, "create_tag", "tag", tag.id, f"name={name}, slug={slug}")
        return {"id": tag.id, "name": tag.name, "slug": tag.slug}

    def update_tag(self, db: Session, tag_id: int, data: dict, operator_id: int) -> dict:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise AppError("Tag not found", 404)
        if "name" in data and data["name"] is not None:
            tag.name = data["name"]
        if "slug" in data and data["slug"] is not None:
            tag.slug = data["slug"]
        db.commit()
        db.refresh(tag)
        self.log(db, operator_id, "update_tag", "tag", tag_id, f"data={data}")
        return {"id": tag.id, "name": tag.name, "slug": tag.slug}

    def delete_tag(self, db: Session, tag_id: int, operator_id: int) -> None:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise AppError("Tag not found", 404)
        db.delete(tag)
        db.commit()
        self.log(db, operator_id, "delete_tag", "tag", tag_id, f"name={tag.name}")

    # ── 评论管理 ──────────────────────────────────────────

    def list_comments(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        article_id: int | None = None,
    ) -> dict:
        query = db.query(Comment).options(
            joinedload(Comment.user),
            joinedload(Comment.article),
        )
        if article_id:
            query = query.filter(Comment.article_id == article_id)

        total = query.count()
        items = query.order_by(Comment.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        seen = set()
        result = []
        for c in items:
            if c.id not in seen:
                seen.add(c.id)
                result.append(
                    {
                        "id": c.id,
                        "content": c.content,
                        "article_id": c.article_id,
                        "user_id": c.user_id,
                        "parent_id": c.parent_id,
                        "created_at": c.created_at.isoformat() if c.created_at else None,
                        "user_name": c.user.name if c.user else None,
                        "article_title": c.article.title if c.article else None,
                    }
                )
        return {
            "items": result,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def delete_comment(self, db: Session, comment_id: int, operator_id: int) -> None:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise AppError("Comment not found", 404)
        db.delete(comment)
        db.commit()
        self.log(db, operator_id, "delete_comment", "comment", comment_id, None)

    # ── 统计面板 ──────────────────────────────────────────

    def get_stats(self, db: Session) -> dict:
        today = date.today().isoformat()

        total_users = db.query(func.count(User.id)).scalar()
        total_articles = db.query(func.count(Article.id)).scalar()
        total_comments = db.query(func.count(Comment.id)).scalar()
        total_categories = db.query(func.count(Category.id)).scalar()
        total_tags = db.query(func.count(Tag.id)).scalar()
        published = db.query(func.count(Article.id)).filter(Article.status == "PUBLISHED").scalar()
        drafts = db.query(func.count(Article.id)).filter(Article.status == "DRAFT").scalar()
        active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()

        today_users = db.query(func.count(User.id)).filter(func.date(User.created_at) == today).scalar()
        today_articles = db.query(func.count(Article.id)).filter(func.date(Article.created_at) == today).scalar()
        today_comments = db.query(func.count(Comment.id)).filter(func.date(Comment.created_at) == today).scalar()

        return {
            "total_users": total_users,
            "total_articles": total_articles,
            "total_comments": total_comments,
            "total_categories": total_categories,
            "total_tags": total_tags,
            "published_articles": published,
            "draft_articles": drafts,
            "active_users": active_users,
            "today_new_users": today_users,
            "today_new_articles": today_articles,
            "today_new_comments": today_comments,
        }

    # ── 操作日志 ──────────────────────────────────────────

    def list_logs(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        action: str | None = None,
    ) -> dict:
        query = db.query(OperationLog)
        if action:
            query = query.filter(OperationLog.action == action)
        total = query.count()
        items = query.order_by(OperationLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return {
            "items": [
                {
                    "id": log.id,
                    "user_id": log.user_id,
                    "action": log.action,
                    "target_type": log.target_type,
                    "target_id": log.target_id,
                    "detail": log.detail,
                    "created_at": log.created_at.isoformat() if log.created_at else None,
                }
                for log in items
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def log(
        self, db: Session, user_id: int, action: str, target_type: str, target_id: int | None, detail: str | None
    ) -> None:
        entry = OperationLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            detail=detail,
        )
        db.add(entry)
        db.commit()

    # ── helpers ───────────────────────────────────────────

    def _user_to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role.value,
            "is_active": user.is_active,
            "avatar": user.avatar,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    def _article_to_dict(self, article: Article) -> dict:
        return {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "status": article.status.value if article.status else "DRAFT",
            "view_count": article.view_count,
            "created_at": article.created_at.isoformat() if article.created_at else None,
            "author_name": article.author.name if article.author else None,
            "category_name": article.category.name if article.category else None,
        }


admin_service = AdminService()
