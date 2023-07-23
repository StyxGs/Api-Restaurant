from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.submenu import SubMenu


class Menu(Base):
    __tablename__ = 'menu'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=str(uuid4()), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String)
    submenu: Mapped[list['SubMenu']] = relationship(cascade='all, delete')

    def __repr__(self) -> str:
        return f'Menu(id={self.id!r}, title={self.title!r})'
