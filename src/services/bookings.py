from src.Schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import UserIdDep
from src.exceptions import ObjectNotFoundException, BookingNotFoundHTTPEException, RoomExistsExceptionHTTPExceptions
from src.services.base import BaseService


class BookingsService(BaseService):

    async def get_bookings(self):

        return await self.db.bookings.get_all()


    async def get_my_bookings(self, user_id:int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, booking_data:BookingAddRequest, user_id: int):

        try:
            room = await self.db.rooms.get_one(id= booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomExistsExceptionHTTPExceptions
        hotel = await self.db.hotels.get_one(id = room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

    async def delete_booking(self, user_id):
        await self.db.bookings.delete(user_id=user_id)
        await self.db.commit()