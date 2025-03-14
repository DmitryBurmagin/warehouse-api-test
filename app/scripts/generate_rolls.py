"""Генерируем рулоны."""
import asyncio
from app.tests.factories.rolls import RollsFactory
from app.core.db import AsyncSessionLocal


async def generate_data():
    """Генерация тестовых данных в БД."""
    async with AsyncSessionLocal() as session:
        RollsFactory._meta.sqlalchemy_session = session
        rolls = RollsFactory.create_batch(10)
        print(f"Создано {len(rolls)} рулонов.")


if __name__ == "__main__":
    asyncio.run(generate_data())
