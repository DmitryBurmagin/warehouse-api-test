"""Фибрики для генерации случайных данных."""

import factory
from app.models.rolls import Rolls


class RollsFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Фабрика для создания тестовых данных Rolls."""

    class Meta:
        """Метакласс."""

        model = Rolls
        sqlalchemy_session = None

    length = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    weight = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True
    )
    added_at = factory.Faker("date_time_this_year")
    removed_at = None
