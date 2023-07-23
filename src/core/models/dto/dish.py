from dataclasses import dataclass

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class DishDTO(BaseDTO):
    price: str

    @property
    def get_price(self):
        return self.price
