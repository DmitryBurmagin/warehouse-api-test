"""
Схема сериализации для модели Rolls.

Этот модуль содержит схемы Pydentic для работы с данными о рулонах.
Схемы используются для создания, обновления и получения информации
о рулонах на складе.
"""

from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class RollsBase(BaseModel):
    """
    Базовая схема для работы с рулонами.

    Описывает общие атрибуты рулонов, такие как длина и вес.
    Используется во всех схемах.
    """

    length: float = Field(..., description="Длина рулонна")
    weight: float = Field(..., description="Вес рулонна")

    class Config:
        """Пример данных schema_extra."""

        schema_extra = {"example": {"length": 5.5, "weight": 100.0}}


class RollsCreate(RollsBase):
    """
    Схема для создания рулона.

    Наследуется от RollsBase, не добавляет новых полей.
    """

    class Config:
        """Пример данных schema_extra."""

        schema_extra = {"example": {"length": 5.5, "weight": 100.0}}


class RollsUpdate(BaseModel):
    """
    Схема для обновления рулона.

    Наследуется от RollsBase, все поля необязательны.
    """

    length: Optional[float] = Field(None, description="Новая длина рулона")
    weight: Optional[float] = Field(None, description="Новый вес рулона")

    class Config:
        """Пример данных schema_extra."""

        schema_extra = {"example": {"length": 6.0, "weight": 120.0}}


class RollsResponse(RollsBase):
    """
    Схема для ответа на запрос о рулоне.

    Наследуется от RollsBase, используется при возврате данных о рулоне,
    включая идентификатор, дату добавления и возможную дату удаления.
    """

    id: int = Field(..., description="Идентификатор рулонна")
    added_at: dt = Field(..., description="Дата добавления рулонна на склад")
    removed_at: Optional[dt] = Field(
        None, description="Дата удаления рулонна со склада"
    )

    class Config:
        """Пример данных schema_extra."""

        schema_extra = {
            "example": {
                "id": 1,
                "length": 5.5,
                "weight": 100.0,
                "added_at": "2024-01-01T12:00:00Z",
                "removed_at": None,
            }
        }
