import json
from typing import Any

import redis

from app.config import settings

redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_timeout=2,
    socket_connect_timeout=2,
)

try:
    redis_client.ping()
    print("Redis connected")
except redis.ConnectionError:
    print("WARNING: Redis connection failed")


class CacheService:
    def get(self, key: str) -> Any | None:
        try:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception:
            pass
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        try:
            redis_client.set(key, json.dumps(value, default=str), ex=ttl)
        except Exception:
            pass

    def delete(self, key: str) -> None:
        try:
            redis_client.delete(key)
        except Exception:
            pass

    def delete_by_pattern(self, pattern: str) -> None:
        try:
            cursor = 0
            while True:
                cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
                if keys:
                    redis_client.delete(*keys)
                if cursor == 0:
                    break
        except Exception:
            pass


cache_service = CacheService()
