from fastapi import APIRouter
from src.Schemas.bookings import  BookingAdd


from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags="Бронирование отелей" )


@router.post("")
async def book_room(data_booking:BookingAdd, db:DBDep, user_id:UserIdDep ):
    data_booking.user_id = user_id
    data_booking.price = await db.rooms.get_current_room_price(room_id = data_booking.room_id )
    await db.bookings.book_room_now(data_booking)
    await db.commit()
    return {"Status": "OK"}
