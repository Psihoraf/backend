

from sqlalchemy import insert, select

from src.Schemas.bookings import Booking

from src.models.bookings import BookingOrm
from src.repositories.base import BaseRepository

class BookingsRepository(BaseRepository):
    model = BookingOrm
    schema = Booking

    async def get_current_room_price(self, room_id):
        query = select(self.model.price).where(self.model.room_id == room_id)
        result = await self.session.execute(query)
        price = result.scalar_one_or_none()
        return price

    async def book_room_now(self, data_booking:Booking, ):

        data_booking.price = self.model.total_cost
        query = insert(self.model).values(**data_booking.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return self.schema.model_validate(model)