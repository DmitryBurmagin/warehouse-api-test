"""Модуль для работы с базой данных через SQLAlchemy."""

import redis.asyncio as aioredis
from app.core.config import settings

redis = aioredis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)
