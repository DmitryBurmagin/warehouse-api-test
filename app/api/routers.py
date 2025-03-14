"""Сборка всех роутеров, единственного роутера."""

from fastapi import APIRouter

from .endpoints.rolls import router as rolls_router
from .endpoints.statistics import router as statistics_router


main_router = APIRouter()


main_router.include_router(rolls_router, prefix="/rolls", tags=["rolls"])
main_router.include_router(
    statistics_router, prefix="/statistics", tags=["statistics"]
)
