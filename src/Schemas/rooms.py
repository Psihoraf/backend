from pydantic import BaseModel, ConfigDict, Field


class RoomModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoomsAdd(RoomModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int




class RoomsResponse(RoomsAdd):
    id:int



