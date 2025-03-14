"""Основное приложение FastAPI."""

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.core.error_handlers import (
    db_exception_handler,
    redis_exception_handler,
    not_found_handler,
)
from app.api.routers import main_router
from app.core.config import settings
from redis.exceptions import ConnectionError as RedisConnectionError

app = FastAPI(title=settings.title, description=settings.description)

app.include_router(main_router)

app.add_exception_handler(SQLAlchemyError, db_exception_handler)
app.add_exception_handler(RedisConnectionError, redis_exception_handler)
app.add_exception_handler(HTTPException, not_found_handler)
