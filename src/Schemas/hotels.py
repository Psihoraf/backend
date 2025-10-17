from pydantic import BaseModel, Field, ConfigDict


class HotelModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class HotelAdd(HotelModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id:int

class HotelPATCH(HotelModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
