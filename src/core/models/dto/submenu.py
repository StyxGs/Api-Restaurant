from dataclasses import dataclass
from uuid import UUID

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class SubMenuDTO(BaseDTO):
    id: UUID | None = None
    dishes_count: int | None = None

    @property
    def get_data(self):
        return dict(id=str(self.id), title=self.title, description=self.description,
                    dishes_count=self.dishes_count)
