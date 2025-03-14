"""Схема для фильтрации рулонов."""
from datetime import date
from typing import Optional
from pydantic_filters import BaseFilter


class RollsFilter(BaseFilter):
    """Схема для фильтрации рулонов."""

    min_length: Optional[float] = None
    max_length: Optional[float] = None

    min_weight: Optional[float] = None
    max_weight: Optional[float] = None

    added_after: Optional[date] = None
    added_before: Optional[date] = None

    removed_after: Optional[date] = None
    removed_before: Optional[date] = None

    model_config = {
        "orm_mode": True,
    }
