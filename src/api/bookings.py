

from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAlreadyHaveBooked, RoomExistsException
from src.Schemas.bookings import BookingAdd, BookingAddRequest

from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование отелей"] )



@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomExistsException
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAlreadyHaveBooked as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}

@router.delete("/delete/me")
async def delete_my_bookings(user_id:UserIdDep, db:DBDep):
    await db.bookings.delete(user_id=user_id)
    return {"status":"ok"}

