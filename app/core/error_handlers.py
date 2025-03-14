"""Обработка ошибок."""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from redis.exceptions import ConnectionError as RedisConnectionError


async def db_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Обработчик ошибок базы данных."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "База данных недоступна"},
    )


async def redis_exception_handler(
    request: Request, exc: RedisConnectionError
) -> JSONResponse:
    """Обработчик ошибок соединения с Redis."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Кэш недоступен"},
    )


async def not_found_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Обработчик ошибок 404."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Ресурс не найден"},
    )
