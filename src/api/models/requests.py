from src.api.models.base import Base
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
