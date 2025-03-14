"""Фильтры."""
from datetime import date
from typing import Optional

from app.schemas.filters import RollsFilter


def get_filter_params(
    id_min: Optional[int] = None,
    id_max: Optional[int] = None,
    length_min: Optional[int] = None,
    length_max: Optional[int] = None,
    weight_min: Optional[int] = None,
    weight_max: Optional[int] = None,
    added_after: Optional[date] = None,
    added_before: Optional[date] = None,
    deleted_after: Optional[date] = None,
    deleted_before: Optional[date] = None,
) -> RollsFilter:
    """Зависимости для фильров."""
    return RollsFilter(
        id_min=id_min,
        id_max=id_max,
        length_min=length_min,
        length_max=length_max,
        weight_min=weight_min,
        weight_max=weight_max,
        added_after=added_after,
        added_before=added_before,
        deleted_after=deleted_after,
        deleted_before=deleted_before,
    )
