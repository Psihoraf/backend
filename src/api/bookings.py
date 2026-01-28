

from fastapi import APIRouter, HTTPException

from src.exceptions import AllRoomsAlreadyHaveBookedException, check_date_to_after_date_from, \
    AllRoomsAlreadyHaveBookedHTTPException, ObjectNotFoundException, BookingNotFoundHTTPEException
from src.Schemas.bookings import BookingAddRequest

from src.api.dependencies import DBDep, UserIdDep
from src.services.bookings import BookingsService


router = APIRouter(prefix="/bookings", tags=["Бронирование отелей"] )

@router.get("")
async def get_bookings(db: DBDep):
    try:
        return await BookingsService(db).get_bookings()
    except ObjectNotFoundException:
        raise BookingNotFoundHTTPEException

@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    try:
        return await BookingsService(db).get_my_bookings(user_id)
    except ObjectNotFoundException:
        raise BookingNotFoundHTTPEException

@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    check_date_to_after_date_from(booking_data.date_from, booking_data.date_to)
    try:
        booking = await BookingsService(db).add_booking(booking_data, user_id)
    except AllRoomsAlreadyHaveBookedException :
        raise AllRoomsAlreadyHaveBookedHTTPException
    return {"status": "OK", "data": booking}


@router.delete("/delete/me")
async def delete_my_bookings(user_id:UserIdDep, db:DBDep):
    try:
        await BookingsService(db).delete_booking(user_id)
    except ObjectNotFoundException:
        raise BookingNotFoundHTTPEException
    return {"status":"ok"}

