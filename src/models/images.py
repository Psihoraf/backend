from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ImagesOrm(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    image_name: Mapped[str] = mapped_column(nullable=False)
    image_bites: Mapped[bytes] = mapped_column(nullable=False)

    hotels: Mapped[list["HotelsOrm"]] = relationship(
        back_populates="images",
        secondary="hotels_images",
    )

class HotelsImagesOrm(Base):
    __tablename__ = "hotels_images"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    image_id: Mapped[int] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"))