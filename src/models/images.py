from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.datastructures import UploadFile

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