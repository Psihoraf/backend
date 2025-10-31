from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.rooms import RoomsOrm


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(String(100))
    location: Mapped[str]

    rooms: Mapped[list["RoomsOrm"]] = relationship(backref="hotels")