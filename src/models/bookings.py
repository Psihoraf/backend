from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "booking"
    id:Mapped[int] = mapped_column(primary_key = True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date_from: Mapped[date] = mapped_column(nullable=False)
    date_to:Mapped[date] = mapped_column(nullable=False)
    price:Mapped[int] = mapped_column(nullable=False)

    @hybrid_property
    def total_cost(self)->int:
        return self.price *(self.date_to-self.date_from).days
