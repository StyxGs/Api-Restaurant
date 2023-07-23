from dataclasses import dataclass
from uuid import UUID

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class MenuDTO(BaseDTO):
    id: UUID | None = None
    submenus_count: int | None = None
    dishes_count: int | None = None
