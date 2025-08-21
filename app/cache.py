import os
import redis.asyncio as aioredis

_redis = None  # Singleton para no abrir múltiples conexiones

async def init_redis():
    global _redis
    if _redis is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        _redis = aioredis.from_url(
            redis_url, encoding="utf-8", decode_responses=True
        )
    return _redis
