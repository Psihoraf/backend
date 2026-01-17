

from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAlreadyHaveBooked, RoomExistsException
from src.Schemas.bookings import BookingAdd, BookingAddRequest

from src.api.dependencies import DBDep, UserIdDep
from src.services.bookings import BookingsService
from src.services.hotels import HotelsService
from src.services.rooms import RoomsService

router = APIRouter(prefix="/bookings", tags=["Бронирование отелей"] )



@router.get("")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingsService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    try:
        booking = await BookingsService(db).add_booking(booking_data, user_id)
    except AllRoomsAlreadyHaveBooked as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    return {"status": "OK", "data": booking}

@router.delete("/delete/me")
async def delete_my_bookings(user_id:UserIdDep, db:DBDep):
    await BookingsService(db).delete_booking(user_id)
    return {"status":"ok"}

