import redis
from fastapi import Request

from app.core.exceptions import AppError
from app.services.cache import redis_client


def rate_limiter(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    key = f"ratelimit:{ip}"

    try:
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, 60)
    except redis.ConnectionError:
        return

    if current > 60:
        raise AppError("Too many requests", 429)
