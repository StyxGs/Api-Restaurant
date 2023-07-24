from uuid import UUID

from pydantic import Field, field_validator

from src.api.models.base import Base


class PyMenu(Base):
    id: UUID
    title: str
    description: str
    submenus_count: int = Field(default=0)
    dishes_count: int = Field(default=0)


class PySubMenu(Base):
    id: UUID
    title: str
    description: str
    dishes_count: int = Field(default=0)


class PyDish(Base):
    id: UUID
    title: str
    description: str
    price: str

    @field_validator('price')
    def validate_birth_date(cls, correct_price):
        correct_price = str(round(float(correct_price), 2))
        return correct_price
