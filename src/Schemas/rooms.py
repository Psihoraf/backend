from pydantic import BaseModel, ConfigDict, Field


class RoomModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoomsAdd:
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    hotel_id: int



class Rooms(RoomsAdd):
    id:int


