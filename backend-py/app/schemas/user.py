from datetime import datetime

from pydantic import BaseModel

from app.models.user import Role


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserBrief(BaseModel):
    id: int
    name: str
    avatar: str | None = None

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: Role
    avatar: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
