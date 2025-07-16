from .database import AsyncSessionLocal
import os
import redis.asyncio as aioredis

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_redis():
    return aioredis.from_url(os.getenv("REDIS_URL"))
