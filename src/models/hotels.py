from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(unique=True, nullable=False)

    images: Mapped[list["ImagesOrm"]] = relationship(
        back_populates="hotels",
        secondary="hotels_images",
    )


