"""Модель руллонов."""
from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Float

from app.core.db import Base


class Rolls(Base):
    """
    Класс модели Rolls представляет собой запись о рулоне металла на складе.

    Атрибуты:
        id (int): Уникальный идентификатор рулона (наследуется с Base).
        length (float): Длина рулона (в метрах).
        weight (float): Вес рулона (в килограммах).
        added_at (datetime): Дата и время добавления рулона на склад.
        removed_at (datetime): Дата и время удаления рулона с склада.
    """

    length = Column(Float, default=0, nullable=False)
    weight = Column(Float, default=0, nullable=False)
    added_at = Column(DateTime, default=dt.utcnow, nullable=False)
    removed_at = Column(DateTime)

    def __repr__(self):
        """
        Представление объекта в строковом виде для удобства отладки.

        Возвращаемое значение:
            str: Форматированная строка с информацией о рулоне.
        """
        return (
            f"<Roll(id={self.id}, length={self.length},"
            f"weight={self.weight}, added_at={self.added_at},"
            f"removed_at={self.removed_at})>"
        )
