from typing import Generator

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.config import settings
from app.core.exceptions import AppError
from app.models.user import User
from app.services.token_blacklist import token_blacklist

security = HTTPBearer()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    if token_blacklist.has(token):
        raise AppError("Token has been revoked", 401)

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise AppError("Invalid or expired token", 401)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppError("User not found", 401)
    return user


def require_role(*roles: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in roles:
            raise AppError("Insufficient permissions", 403)
        return user

    return checker
