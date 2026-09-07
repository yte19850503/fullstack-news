from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.services.article import ArticleService

router = APIRouter(prefix="/articles", tags=["articles"])
article_service = ArticleService()


@router.get("/", summary="文章列表（分页、筛选、排序）")
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: int | None = None,
    status: str | None = None,
    q: str | None = Query(None, max_length=200),
    tag_id: int | None = None,
    author_id: int | None = None,
    date_from: str | None = Query(None, description="起始日期 YYYY-MM-DD"),
    date_to: str | None = Query(None, description="结束日期 YYYY-MM-DD"),
    sort: str = Query("newest", pattern="^(newest|popular)$"),
    db: Session = Depends(get_db),
):
    return article_service.list(
        db,
        page,
        page_size,
        category_id,
        status,
        q,
        tag_id,
        author_id,
        date_from,
        date_to,
        sort,
    )


@router.get("/search", summary="全文搜索文章")
def search_articles(
    q: str = Query(..., min_length=1, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return article_service.search_fulltext(db, q, page, page_size)


@router.get("/hot-search-terms", summary="热门搜索词 Top N")
def hot_search_terms(top: int = Query(10, ge=1, le=50)):
    return article_service.get_hot_search_terms(top)


@router.get("/{slug}", summary="根据 slug 获取文章详情")
def get_article(slug: str, db: Session = Depends(get_db)):
    return article_service.get_by_slug(db, slug)


@router.post("/", summary="创建文章（需 EDITOR/ADMIN）")
def create_article(
    body: ArticleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("EDITOR", "ADMIN")),
):
    return article_service.create(db, body.model_dump(), user.id)


@router.put("/{article_id}", summary="更新文章（需 EDITOR/ADMIN）")
def update_article(
    article_id: int,
    body: ArticleUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("EDITOR", "ADMIN")),
):
    return article_service.update(db, article_id, body.model_dump(exclude_unset=True))


@router.delete("/{article_id}", summary="删除文章（需 ADMIN）")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    article_service.delete(db, article_id)
    return {"message": "Deleted"}
