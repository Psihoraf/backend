from pydantic import BaseModel, ConfigDict, Field, validator, field_validator

from src.Schemas.facilities import Facility


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

    @field_validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Цена не может быть отрицательной')
        return v

    @field_validator('quantity')
    def validate_nights_count(cls, v):
        if v <= 0:
            raise ValueError('Количество номеров должно быть положительным')
        return v

    @field_validator('title')
    @classmethod
    def strip_and_validate(cls, v):
        if v is not None:
            v = v.strip()

            if len(v) < 1:
                raise ValueError("Поле не может быть пустым")
        return v

class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

class Rooms(RoomsAdd):
    id:int

class RoomsWithRels(Rooms):
    facilities: list[Facility]



