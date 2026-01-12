from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


from src.database import Base


class ImagesOrm(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    image_name: Mapped[str]
    image_bites: Mapped[bytes]


class HotelsImagesOrm(Base):
    __tablename__ = "hotels_images"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    image_id: Mapped[int] = mapped_column(ForeignKey("images.id"))