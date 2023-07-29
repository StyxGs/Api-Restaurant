from pydantic import Field, field_validator

from src.api.models.base import Base
from src.core.models.dto.dish import DishDTO
from src.core.models.dto.menu import MenuDTO
from src.core.models.dto.submenu import SubMenuDTO


class BaseMenuAndSubmenu(Base):
    title: str
    description: str


class RQSTMenu(BaseMenuAndSubmenu):

    def to_dto(self):
        return MenuDTO(title=self.title, description=self.description)


class RQSTSubMenu(BaseMenuAndSubmenu):

    def to_dto(self):
        return SubMenuDTO(title=self.title, description=self.description)


class RQSTDish(BaseMenuAndSubmenu):
    price: str = Field(examples=['14.45', ])

    @field_validator('price')
    def validate_birth_date(cls, correct_price):
        float(correct_price)
        return correct_price

    def to_dto(self):
        return DishDTO(title=self.title, description=self.description, price=self.price)
