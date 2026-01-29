from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.Schemas.rooms import Rooms


class HotelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class HotelAdd(BaseModel):
    title: str = Field(min_length=1)
    location: str = Field(min_length=1)


class HotelAddWithImage(HotelModel):
    title: str
    location: str
    image_name: str  | None = Field(None)

class Hotel(HotelAdd):
    id:int
class HotelResponse(HotelAdd):
    rooms: list[Rooms] = []

class HotelPATCH(HotelModel):
    title: str = None
    location: str = None

    @field_validator('title', 'location')
    @classmethod
    def strip_and_validate(cls, v):
        if v is not None:
            v = v.strip()

            if len(v) < 1:
                raise ValueError("Поле не может быть пустым")
        return v


class ImageAddIntoBD(BaseModel):
    image_name: str
    image_bites: bytes
