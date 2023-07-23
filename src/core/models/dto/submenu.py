from dataclasses import dataclass
from uuid import UUID

from src.core.models.dto.base_dto import BaseDTO


@dataclass
class SubMenuDTO(BaseDTO):
    id: UUID | None = None
    dishes_count: int | None = None
