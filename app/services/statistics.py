"""Сбор статистики."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, case
from datetime import date, timedelta
import json
import logging
from typing import Optional

from app.models.rolls import Rolls
from app.core.redis import redis


class StatisticsService:
    """Сервис для получения статистики по роллам с кэшем Redis."""

    def __init__(self, session: AsyncSession):
        """Инициализация сервиса статистики."""
        self.db = session

    @staticmethod
    def format_number(value, decimals=2):
        """Форматирует число: округляет и добавляет пробелы."""
        if value is None:
            return "Нет данных"
        return f"{round(value, decimals):,}".replace(",", " ")

    @staticmethod
    def format_timedelta(value):
        """Форматирует timedelta в удобный вид."""
        if not value:
            return "Нет данных"

        total_seconds = value.total_seconds()
        days = int(total_seconds // 86400)
        hours = int((total_seconds % 86400) // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        parts = []
        if days:
            parts.append(f"{days} д.")
        if hours:
            parts.append(f"{hours} ч.")
        if minutes:
            parts.append(f"{minutes} мин.")
        if seconds or not parts:
            parts.append(f"{seconds} сек.")

        return " ".join(parts)

    def _get_cache_key(self, start_date: date, end_date: date):
        """Формирует ключ кэша."""
        return f"stats:{start_date}:{end_date}"

    async def get_statistics(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        """Получает статистику, используя кэш Redis (10 мин)."""
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=7)

        cache_key = self._get_cache_key(start_date, end_date)

        cached_data = await redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        stmt = select(
            func.count(case((Rolls.added_at >= start_date, Rolls.id))).label(
                "added_count"
            ),
            func.count(case((Rolls.removed_at.isnot(None), Rolls.id))).label(
                "removed_count"
            ),
            func.avg(Rolls.length).label("avg_length"),
            func.avg(Rolls.weight).label("avg_weight"),
            func.min(Rolls.length).label("min_length"),
            func.max(Rolls.length).label("max_length"),
            func.min(Rolls.weight).label("min_weight"),
            func.max(Rolls.weight).label("max_weight"),
            func.sum(Rolls.weight).label("total_weight"),
            func.min(Rolls.removed_at - Rolls.added_at).label(
                "min_storage_time"
            ),
            func.max(Rolls.removed_at - Rolls.added_at).label(
                "max_storage_time"
            ),
        )

        result_proxy = await self.db.execute(stmt)
        stats = result_proxy.one()

        result = {
            "Добавлено": self.format_number(stats.added_count, 0),
            "Удалено": self.format_number(stats.removed_count, 0),
            "Средняя длина": self.format_number(stats.avg_length),
            "Средний вес": self.format_number(stats.avg_weight),
            "Минимальная длина": self.format_number(stats.min_length),
            "Максимальная длина": self.format_number(stats.max_length),
            "Минимальный вес": self.format_number(stats.min_weight),
            "Максимальный вес": self.format_number(stats.max_weight),
            "Общий вес": self.format_number(stats.total_weight),
            "Минимальный промежуток хранения": self.format_timedelta(
                stats.min_storage_time
            ),
            "Максимальный промежуток хранения": self.format_timedelta(
                stats.max_storage_time
            ),
        }

        try:
            await redis.set(
                cache_key, json.dumps(result, ensure_ascii=False), ex=600
            )
        except Exception as e:
            logging.error(f"Ошибка при записи в Redis: {e}")

        return result

    async def invalidate_cache(self):
        """Удаляет все кэши статистики."""
        try:
            keys = await redis.keys("stats:*")
            if keys:
                await redis.delete(*keys)
        except Exception as e:
            logging.error(f"Ошибка при очистке кэша: {e}")
