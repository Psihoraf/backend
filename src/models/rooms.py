import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database import Base
if typing.TYPE_CHECKING:
    from src.models import FacilitiesOrm

class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)


    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities",
    )