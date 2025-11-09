

from sqlalchemy import insert, select

from src.Schemas.bookings import Booking, BookingAdd

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_bookings_of_user_id(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]