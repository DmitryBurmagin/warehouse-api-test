"""Сборка всех роутеров, единственного роутера."""

from fastapi import APIRouter

from .rolls import router as rolls_router


main_router = APIRouter()


main_router.include_router(rolls_router, tags=["rolls"])
