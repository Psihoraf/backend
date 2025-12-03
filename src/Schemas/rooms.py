from pydantic import BaseModel, ConfigDict, Field


class RoomModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)





class RoomsAdd(RoomModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int  | None = None
    quantity: int | None = None
    facilities_ids: list[int] | None = []

class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class RoomsResponse(RoomsAdd):
    id:int



