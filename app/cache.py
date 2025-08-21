import redis.asyncio as redis
import os

async def init_redis():
    return redis.from_url(
        os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        encoding="utf-8",
        decode_responses=True
    )
