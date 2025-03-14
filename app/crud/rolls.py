"""CRUD, для модели Rolls."""

from typing import Generic, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.filters import RollsFilter

from app.core.db import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDbase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый CRUD-класс для работы с моделями SQLAlchemy.

    Generic:
        - ModelType: SQLAlchemy-модель (должна наследоваться от `Base`).
        - CreateSchemaType: Pydantic-схема для создания объекта.
        - UpdateSchemaType: Pydantic-схема для обновления объекта.
    """

    def __init__(self, model: Type[ModelType]):
        """Инициализирует CRUD-класс."""
        self.model = model

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        """
        Получает объект из базы данных по его ID.

        Args:
            - obj_id (int): ID объекта.
            - session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            - Optional[ModelType]: Найденный объект или None.
        """
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """
        Создаёт новый объект в базе данных.

        Args:
            - obj_in (CreateSchemaType): Pydantic-схема с данными для создания.
            - session (AsyncSession): Асинхронная сессия SQLAlchemy.
            - commit (bool): Нужно ли коммитить изменения.

        Returns:
            - ModelType: Созданный объект.
        """
        obj_in_data = obj_in.model_dump()

        db_obj = self.model(**obj_in_data)
        session.add(db_obj)

        if commit:
            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db_obj,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """
        Обновляет существующий объект в базе данных.

        Args:
            - db_obj (ModelType): Объект, который нужно обновить.
            - obj_in (UpdateSchemaType): Pydantic-схема с новыми данными.
            - session (AsyncSession): Асинхронная сессия SQLAlchemy.
            - commit (bool): Нужно ли коммитить изменения.

        Returns:
            - ModelType: Обновленный объект.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])

        if commit:
            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    async def remove(self, db_obj, session: AsyncSession) -> ModelType:
        """
        Удаляет объект из базы данных.

        Args:
            db_obj (ModelType): Объект, который нужно удалить.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Optional[ModelType]: Удалённый объект или None.
        """
        await session.delete(db_obj)
        await session.commit()

        return db_obj

    async def filter(
        self, session: AsyncSession, filters: RollsFilter
    ) -> list[ModelType]:
        """
        Фильтрует объекты по переданным параметрам.

        Args:
            - session (AsyncSession): Асинхронная сессия SQLAlchemy.
            - filters (RollsFilter): Объект фильтров.

        Returns:
            - list[ModelType]: Найденные объекты.
        """
        query = select(self.model)

        if filters.min_length is not None:
            query = query.where(self.model.length >= filters.min_length)
        if filters.max_length is not None:
            query = query.where(self.model.length <= filters.max_length)

        if filters.min_weight is not None:
            query = query.where(self.model.weight >= filters.min_weight)
        if filters.max_weight is not None:
            query = query.where(self.model.weight <= filters.max_weight)

        if filters.added_after is not None:
            query = query.where(self.model.added_at >= filters.added_after)
        if filters.added_before is not None:
            query = query.where(self.model.added_at <= filters.added_before)

        if filters.removed_after is not None:
            query = query.where(self.model.removed_at >= filters.removed_after)
        if filters.removed_before is not None:
            query = query.where(
                self.model.removed_at <= filters.removed_before
            )

        result = await session.execute(query)
        return result.scalars().all()
