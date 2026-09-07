from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", summary="用户注册")
def register(body: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, body.email, body.password, body.name)


@router.post("/login", summary="用户登录，返回 JWT token")
def login(body: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, body.email, body.password)


@router.post("/logout", summary="用户登出，使 token 失效")
def logout(request: Request, user: User = Depends(get_current_user)):
    token = request.headers.get("authorization", "").removeprefix("Bearer ")
    auth_service.logout(token)
    return {"message": "Logged out successfully"}
