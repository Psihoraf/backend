from datetime import date

from sqlalchemy import insert, select

from src.Schemas.bookings import Booking, BookingAdd

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper


    async def get_bookings_with_today_checkin(self):
        query =(
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
