from app.services.cache import redis_client


class TokenBlacklistService:
    def add(self, token: str, ttl_seconds: int) -> None:
        try:
            redis_client.setex(f"token:blacklist:{token}", ttl_seconds, "1")
        except Exception:
            pass

    def has(self, token: str) -> bool:
        try:
            return redis_client.exists(f"token:blacklist:{token}") > 0
        except Exception:
            return False


token_blacklist = TokenBlacklistService()
