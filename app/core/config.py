"""Конфигурация приложения."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта, передаваемые из env."""

    title: str = "WareHouse API"
    description: str = (
        "Тестовое задание для Северстали | Backend"
        " на FastAPI для управления складом рулонов металла"
    )

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    database_url: str

    redis_host: str
    redis_port: int
    redis_db: int = 0

    debug: bool = True
    secret_key: str

    class Config:
        """Передача из env."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
