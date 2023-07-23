from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[str] = mapped_column(String(10))
    submenu_id: Mapped[UUID] = mapped_column(ForeignKey('submenu.id', ondelete='CASCADE'))

    def __repr__(self) -> str:
        return f'Dish(id={self.id!r}, title={self.title!r}, price={self.price!r})'
