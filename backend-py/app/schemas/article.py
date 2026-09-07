from datetime import datetime

from pydantic import BaseModel

from app.models.article import ArticleStatus
from app.schemas.user import UserBrief
from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse


class ArticleCreate(BaseModel):
    title: str
    content: str
    summary: str | None = None
    cover_image: str | None = None
    category_id: int
    tag_ids: list[int] | None = None
    status: ArticleStatus = ArticleStatus.DRAFT


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    summary: str | None = None
    cover_image: str | None = None
    category_id: int | None = None
    status: ArticleStatus | None = None
    tag_ids: list[int] | None = None


class ArticleBrief(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None = None
    cover_image: str | None = None
    status: ArticleStatus
    view_count: int
    created_at: datetime
    updated_at: datetime
    author: UserBrief
    category: CategoryResponse
    tags: list[TagResponse] = []

    model_config = {"from_attributes": True}


class ArticleResponse(ArticleBrief):
    content: str
