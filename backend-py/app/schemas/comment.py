from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserBrief


class CommentCreate(BaseModel):
    content: str
    article_id: int
    parent_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    content: str
    article_id: int
    user_id: int
    parent_id: int | None = None
    created_at: datetime
    user: UserBrief
    replies: list["CommentResponse"] = []

    model_config = {"from_attributes": True}
