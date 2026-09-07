import re
import time

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.article import Article
from app.core.exceptions import AppError


def _to_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fa5]+", "-", name.lower()).strip("-")
    return f"{slug}-{int(time.time() * 1000):x}"


class CategoryService:
    def list(self, db: Session) -> list[dict]:
        categories = db.query(Category).all()
        result = []
        for cat in categories:
            count = db.query(Article).filter(Article.category_id == cat.id).count()
            result.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "description": cat.description,
                    "article_count": count,
                }
            )
        return result

    def create(self, db: Session, name: str, description: str | None = None) -> dict:
        slug = _to_slug(name)
        cat = Category(name=name, slug=slug, description=description)
        db.add(cat)
        db.commit()
        db.refresh(cat)
        return {"id": cat.id, "name": cat.name, "slug": cat.slug, "description": cat.description}

    def update(self, db: Session, category_id: int, name: str | None = None, description: str | None = None) -> dict:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            raise AppError("Category not found", 404)
        if name:
            cat.name = name
            cat.slug = _to_slug(name)
        if description is not None:
            cat.description = description
        db.commit()
        db.refresh(cat)
        return {"id": cat.id, "name": cat.name, "slug": cat.slug, "description": cat.description}

    def delete(self, db: Session, category_id: int) -> None:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            raise AppError("Category not found", 404)
        db.delete(cat)
        db.commit()
