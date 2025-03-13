"""Модуль для работы с базой данных через SQLAlchemy."""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, declared_attr

from app.core.config import settings


class PreBase:
    """Основной класс для определения таблиц."""

    @declared_attr
    def __tablename__(cls):
        """Автоматически генерирует имя таблицы на основе имени класса."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    """Генератор для получения асинхронной сессии базы данных."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
