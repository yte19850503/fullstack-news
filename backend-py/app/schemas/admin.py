from datetime import datetime

from pydantic import BaseModel

from app.models.user import Role


class UserUpdate(BaseModel):
    name: str | None = None
    role: Role | None = None


class UserToggleActive(BaseModel):
    is_active: bool


class AdminUserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: Role
    is_active: bool
    avatar: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TagCreate(BaseModel):
    name: str
    slug: str


class TagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class CommentAdminResponse(BaseModel):
    id: int
    content: str
    article_id: int
    user_id: int
    parent_id: int | None = None
    created_at: datetime
    user_name: str | None = None
    article_title: str | None = None

    model_config = {"from_attributes": True}


class OperationLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    target_type: str
    target_id: int | None = None
    detail: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    total_users: int
    total_articles: int
    total_comments: int
    total_categories: int
    total_tags: int
    published_articles: int
    draft_articles: int
    active_users: int
    today_new_users: int
    today_new_articles: int
    today_new_comments: int
