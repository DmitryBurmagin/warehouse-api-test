"""Фильтры."""

from datetime import date
from typing import Optional, Annotated
from fastapi import Query

from app.schemas.filters import RollsFilter


def get_filter_params(
    min_length: Annotated[
        Optional[float],
        Query(description="Минимальная длина рулона (м)", example=10.5, ge=0),
    ] = None,
    max_length: Annotated[
        Optional[float],
        Query(description="Максимальная длина рулона (м)", example=20.0, ge=0),
    ] = None,
    min_weight: Annotated[
        Optional[float],
        Query(description="Минимальный вес рулона (кг)", example=150.0, gt=0),
    ] = None,
    max_weight: Annotated[
        Optional[float],
        Query(description="Максимальный вес рулона (кг)", example=300.0, gt=0),
    ] = None,
    added_after: Annotated[
        Optional[date],
        Query(
            description="Фильтр по дате добавления (>=)", example="2024-01-01"
        ),
    ] = None,
    added_before: Annotated[
        Optional[date],
        Query(
            description="Фильтр по дате добавления (<=)", example="2024-12-31"
        ),
    ] = None,
    removed_after: Annotated[
        Optional[date],
        Query(
            description="Фильтр по дате удаления (>=)", example="2024-06-01"
        ),
    ] = None,
    removed_before: Annotated[
        Optional[date],
        Query(
            description="Фильтр по дате удаления (<=)", example="2024-06-30"
        ),
    ] = None,
) -> RollsFilter:
    """
    Зависимость для фильтрации рулонов.

    Возвращает:
        RollsFilter: Объект фильтра с применёнными параметрами.
    """
    return RollsFilter(
        min_length=min_length,
        max_length=max_length,
        min_weight=min_weight,
        max_weight=max_weight,
        added_after=added_after,
        added_before=added_before,
        removed_after=removed_after,
        removed_before=removed_before,
    )
