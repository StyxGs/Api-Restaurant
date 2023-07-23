from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.dish import Dish


class SubMenu(Base):
    __tablename__ = 'submenu'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    menu_id: Mapped[UUID] = mapped_column(ForeignKey('menu.id'))
    dishes: Mapped[list['Dish']] = relationship(cascade='all, delete')
