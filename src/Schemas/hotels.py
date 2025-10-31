from pydantic import BaseModel, Field, ConfigDict

from src.Schemas.rooms import RoomsResponse


class HotelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class HotelAdd(HotelModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id:int
class HotelResponse(HotelAdd):
    rooms: list[RoomsResponse] = []

class HotelPATCH(HotelModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
