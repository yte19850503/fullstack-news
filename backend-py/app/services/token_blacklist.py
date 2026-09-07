from app.services.cache import redis_client


class TokenBlacklistService:
    def add(self, token: str, ttl_seconds: int) -> None:
        redis_client.setex(f"token:blacklist:{token}", ttl_seconds, "1")

    def has(self, token: str) -> bool:
        return redis_client.exists(f"token:blacklist:{token}") > 0


token_blacklist = TokenBlacklistService()
