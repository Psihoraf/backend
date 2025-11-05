from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BookingAdd(BookingModel):

    room_id:int
    user_id:int
    date_from: date
    date_to: date
    price: int

class Booking(BookingAdd):
    id: int

class BookingPOST(BaseModel):
    room_id: int
    date_from: date
    date_to: date
