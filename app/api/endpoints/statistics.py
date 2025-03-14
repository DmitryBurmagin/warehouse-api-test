"""Модуль API-роутов для работы с ."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime as dt

from app.services.statistics import StatisticsService
from app.core.db import get_async_session

router = APIRouter()


@router.get("/")
async def get_statistics(
    start_date: dt | None = Query(
        None, description="Начальная дата (опционально)"
    ),
    end_date: dt | None = Query(
        None, description="Конечная дата (опционально)"
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт статистики."""
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date должен быть меньше end_date",
        )
    service = StatisticsService(session)
    return await service.get_statistics(start_date, end_date)
