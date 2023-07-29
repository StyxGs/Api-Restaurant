from dataclasses import dataclass
from uuid import UUID

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class DishDTO(BaseDTO):
    id: UUID | None = None
    price: str | None = None

    @property
    def get_data(self):
        dto = dict(title=self.title, description=self.description, price=self.price)
        return {name: data for name, data in dto.items() if data}
