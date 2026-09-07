import json
from typing import Any

import redis

from app.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

try:
    redis_client.ping()
    print("Redis connected")
except redis.ConnectionError:
    print("WARNING: Redis connection failed")


class CacheService:
    def get(self, key: str) -> Any | None:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        redis_client.set(key, json.dumps(value, default=str), ex=ttl)

    def delete(self, key: str) -> None:
        redis_client.delete(key)

    def delete_by_pattern(self, pattern: str) -> None:
        cursor = 0
        while True:
            cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
            if keys:
                redis_client.delete(*keys)
            if cursor == 0:
                break


cache_service = CacheService()
