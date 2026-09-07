from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db, require_role
from app.core.exceptions import AppError
from app.models.article import Article, ArticleTag
from app.models.user import User
from app.schemas.admin import (
    UserUpdate,
    UserToggleActive,
    TagCreate,
    TagUpdate,
)
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.services.admin import admin_service
from app.services.article import ArticleService

router = APIRouter(prefix="/admin", tags=["admin"])


# ── 统计面板 ──────────────────────────────────────────────


@router.get("/stats", summary="后台统计面板数据")
def get_stats(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.get_stats(db)


# ── 用户管理 ──────────────────────────────────────────────


@router.get("/users", summary="用户列表（分页、筛选）")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.list_users(db, page, page_size, role, q)


@router.put("/users/{user_id}", summary="修改用户信息")
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    operator: User = Depends(require_role("ADMIN")),
):
    return admin_service.update_user(db, user_id, body.model_dump(exclude_unset=True), operator.id)


@router.put("/users/{user_id}/toggle-active", summary="启用/禁用用户")
def toggle_user_active(
    user_id: int,
    body: UserToggleActive,
    db: Session = Depends(get_db),
    operator: User = Depends(require_role("ADMIN")),
):
    return admin_service.toggle_user_active(db, user_id, body.is_active, operator.id)


# ── 文章管理 ──────────────────────────────────────────────

article_service = ArticleService()


@router.get("/articles", summary="文章管理列表")
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN", "EDITOR")),
):
    return admin_service.list_articles(db, page, page_size, status, q)


@router.post("/articles", summary="创建文章")
def create_article(
    body: ArticleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("EDITOR", "ADMIN")),
):
    return article_service.create(db, body.model_dump(), user.id)


@router.post("/articles/batch-update", summary="批量变更文章状态")
def batch_update_articles(
    article_ids: list[int],
    status: str = Query(..., pattern="^(DRAFT|PUBLISHED|ARCHIVED)$"),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN", "EDITOR")),
):
    return admin_service.batch_update_articles(db, article_ids, status, user.id)


@router.put("/articles/{article_id}/review", summary="审核文章（变更状态）")
def review_article(
    article_id: int,
    status: str = Query(..., pattern="^(DRAFT|PUBLISHED|ARCHIVED)$"),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN", "EDITOR")),
):
    return admin_service.review_article(db, article_id, status, user.id)


@router.get("/articles/{article_id}", summary="获取文章详情（编辑回填用）")
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN", "EDITOR")),
):
    article = (
        db.query(Article)
        .options(
            joinedload(Article.author),
            joinedload(Article.category),
            joinedload(Article.tags).joinedload(ArticleTag.tag),
        )
        .filter(Article.id == article_id)
        .first()
    )
    if not article:
        raise AppError("Article not found", 404)
    return article_service._to_detail(article)


@router.put("/articles/{article_id}", summary="更新文章")
def update_article(
    article_id: int,
    body: ArticleUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("EDITOR", "ADMIN")),
):
    return article_service.update(db, article_id, body.model_dump(exclude_unset=True))


@router.delete("/articles/{article_id}", summary="删除文章")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    article_service.delete(db, article_id)
    return {"message": "Deleted"}


# ── 分类管理 ──────────────────────────────────────────────


@router.get("/categories", summary="分类列表")
def list_categories(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.list_categories(db)


@router.post("/categories", summary="创建分类")
def create_category(
    name: str = Query(...),
    description: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.create_category(db, name, description, user.id)


@router.put("/categories/{category_id}", summary="更新分类")
def update_category(
    category_id: int,
    name: str | None = Query(None),
    description: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.update_category(db, category_id, name, description, user.id)


@router.delete("/categories/{category_id}", summary="删除分类")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    admin_service.delete_category(db, category_id, user.id)
    return {"message": "Deleted"}


# ── 标签管理 ──────────────────────────────────────────────


@router.get("/tags", summary="标签列表")
def list_tags(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.list_tags(db)


@router.post("/tags", summary="创建标签")
def create_tag(
    body: TagCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.create_tag(db, body.name, body.slug, user.id)


@router.put("/tags/{tag_id}", summary="更新标签")
def update_tag(
    tag_id: int,
    body: TagUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.update_tag(db, tag_id, body.model_dump(exclude_unset=True), user.id)


@router.delete("/tags/{tag_id}", summary="删除标签")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    admin_service.delete_tag(db, tag_id, user.id)
    return {"message": "Deleted"}


# ── 评论管理 ──────────────────────────────────────────────


@router.get("/comments", summary="评论管理列表")
def list_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    article_id: int | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.list_comments(db, page, page_size, article_id)


@router.delete("/comments/{comment_id}", summary="删除评论")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    admin_service.delete_comment(db, comment_id, user.id)
    return {"message": "Deleted"}


# ── 操作日志 ──────────────────────────────────────────────


@router.get("/logs", summary="操作日志列表")
def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("ADMIN")),
):
    return admin_service.list_logs(db, page, page_size, action)
