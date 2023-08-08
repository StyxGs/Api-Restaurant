from dataclasses import dataclass
from uuid import UUID

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class DishDTO(BaseDTO):
    id: UUID | None = None
    price: str | None = None

    @property
    def get_data(self) -> dict:
        return dict(id=str(self.id), title=self.title, description=self.description, price=self.price)

    @property
    def get_data_without_none(self) -> dict:
        dto = dict(title=self.title, description=self.description, price=self.price)
        return {name: data for name, data in dto.items() if data}
