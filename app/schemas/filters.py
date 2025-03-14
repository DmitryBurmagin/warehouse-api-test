"""Схема фильтров."""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class RollsFilter(BaseModel):
    """Схема для фильтрации рулона."""

    id_min: Optional[int] = Field(None, description="Минимальный ID")
    id_max: Optional[int] = Field(None, description="Максимальный ID")
    length_min: Optional[int] = Field(None, description="Минимальная длина")
    length_max: Optional[int] = Field(None, description="Максимальная длина")
    weight_min: Optional[int] = Field(None, description="Минимальный вес")
    weight_max: Optional[int] = Field(None, description="Максимальный вес")
    added_after: Optional[date] = Field(
        None, description="Дата добавления после"
    )
    added_before: Optional[date] = Field(
        None, description="Дата добавления до"
    )
    deleted_after: Optional[date] = Field(
        None, description="Дата удаления после"
    )
    deleted_before: Optional[date] = Field(
        None, description="Дата удаления до"
    )
