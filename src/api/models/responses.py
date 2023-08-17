from uuid import UUID

from pydantic import Field, field_validator

from src.api.models.base import Base


class BaseResponse(Base):
    id: UUID
    title: str
    description: str


class PyMenu(BaseResponse):
    submenus_count: int = 0
    dishes_count: int = 0


class PySubMenu(BaseResponse):
    dishes_count: int = 0


class PyDish(BaseResponse):
    price: str = Field(examples=['14.45', ])
    discount: int

    @field_validator('price')
    def validate_birth_date(cls, correct_price):
        correct_price = str(round(float(correct_price), 2))
        return correct_price


class Dish(BaseResponse):
    price: str = Field(examples=['14.45', ])


class Submenu(BaseResponse):
    dishes: list[Dish]


class FullMenu(BaseResponse):
    submenus: list[Submenu]
