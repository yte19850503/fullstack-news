from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import AppError
from app.core.sanitizer import validate_password_strength
from app.services.token_blacklist import token_blacklist


class AuthService:
    def register(self, db: Session, email: str, password: str, name: str) -> dict:
        validate_password_strength(password)

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise AppError("Email already registered", 400)

        user = User(
            email=email,
            password=hash_password(password),
            name=name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id, user.email, user.role.value)
        return {"token": token}

    def login(self, db: Session, email: str, password: str) -> dict:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            raise AppError("Invalid email or password", 401)

        token = create_access_token(user.id, user.email, user.role.value)
        return {"token": token}

    def logout(self, token: str) -> None:
        from app.core.security import decode_token
        from datetime import datetime, timezone

        try:
            payload = decode_token(token)
            exp = payload.get("exp", 0)
            ttl = exp - int(datetime.now(timezone.utc).timestamp())
            if ttl > 0:
                token_blacklist.add(token, ttl)
        except Exception:
            pass
