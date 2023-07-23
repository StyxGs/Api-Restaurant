from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.dish import Dish


class SubMenu(Base):
    __tablename__ = 'submenu'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    menu_id: Mapped[UUID] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'))
    dishes: Mapped[list['Dish']] = relationship(cascade='all, delete')

    def __repr__(self) -> str:
        return f'SubMenu(id={self.id!r}, title={self.title!r})'
