from uuid import UUID

from pydantic import Field

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
