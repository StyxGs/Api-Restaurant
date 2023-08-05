from dataclasses import dataclass
from uuid import UUID

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class MenuDTO(BaseDTO):
    id: UUID | None = None
    submenus_count: int | None = None
    dishes_count: int | None = None

    @property
    def get_data(self):
        return dict(id=str(self.id), title=self.title, description=self.description, submenus_count=self.submenus_count,
                    dishes_count=self.dishes_count)
