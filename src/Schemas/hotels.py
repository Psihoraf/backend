from pydantic import BaseModel, Field, ConfigDict

from src.Schemas.rooms import Rooms


class HotelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class HotelAdd(HotelModel):
    title: str
    location: str


class HotelAddWithImage(HotelModel):
    title: str
    location: str
    image_name: str  | None = Field(None)

class Hotel(HotelAdd):
    id:int
class HotelResponse(HotelAdd):
    rooms: list[Rooms] = []

class HotelPATCH(HotelModel):
    title: str | None = Field(None)
    location: str | None = Field(None)


class ImageAddIntoBD(BaseModel):
    image_name: str
    image_bites: bytes
