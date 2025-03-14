"""Модуль API-роутов для работы с рулонами металла."""
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.db import get_async_session
from app.models.rolls import Rolls

from app.schemas.rolls import RollsCreate, RollsUpdate, RollsResponse
from app.schemas.filters import RollsFilter
from app.crud.rolls import CRUDbase
from app.api.dependencies.filters import get_filter_params

router = APIRouter()
crud_rolls = CRUDbase[Rolls, RollsCreate, RollsUpdate](Rolls)


@router.get(
    "/", response_model=List[RollsResponse], response_model_exclude_none=True
)
async def get_rolls(
    session: AsyncSession = Depends(get_async_session),
    filters: Optional[RollsFilter] = Depends(get_filter_params),
) -> List[RollsResponse]:
    """
    Получить информацию о рулоне по его ID.

    Args:
        - roll_id (int): ID рулона.
        - session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        - List[RollsResponse]: Список рулонов, подходящих под фильтр.
    """
    if filters is None:
        filters = RollsFilter()

    return await crud_rolls.filter(session, filters=filters)


@router.get(
    "/{roll_id}",
    response_model=RollsResponse,
    response_model_exclude_none=True,
)
async def get_roll_by_id(
    roll_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> RollsResponse:
    """Получить рулон по его ID."""
    roll = await crud_rolls.get(roll_id, session)
    if not roll:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Рулон не найден"
        )
    return roll


@router.post("/", response_model=RollsCreate, response_model_exclude_none=True)
async def create_rolls(
    roll: RollsCreate, session: AsyncSession = Depends(get_async_session)
) -> RollsResponse:
    """
    Создать новый рулон.

    Args:
        - roll (RollsCreate): Данные для создания рулона.
        - session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        - RollsResponse: Данные созданного рулона.
    """
    return await crud_rolls.create(roll, session)


@router.patch(
    "/{roll_id}", response_model=RollsUpdate, response_model_exclude_none=True
)
async def update_roll(
    roll_id: int,
    roll_in: RollsUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> RollsResponse:
    """
    Обновить данные рулона.

    Args:
        - roll_id (int): ID рулона для обновления.
        - roll_in (RollsUpdate): Новые данные рулона.
        - session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        - RollsResponse: Обновлённые данные рулона.
    """
    db_roll = await crud_rolls.get(roll_id, session)
    if not db_roll:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Рулон не найден"
        )
    return await crud_rolls.update(db_roll, roll_in, session)


@router.delete(
    "/{roll_id}",
    response_model=RollsResponse,
    response_model_exclude_none=True,
)
async def delete_roll(
    roll_id: int, session: AsyncSession = Depends(get_async_session)
) -> RollsResponse:
    """
    Удалить рулон по ID.

    Args:
        - roll_id (int): ID рулона для удаления.
        - session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        - RollsResponse: Данные удалённого рулона.
    """
    db_roll = await crud_rolls.get(roll_id, session)
    if not db_roll:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Рулон не найден"
        )
    return await crud_rolls.remove(db_roll, session)
