from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, insert

from src.Schemas.hotels import Hotel
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async  def get_all(self, location, title, limit, offset ):

         async with async_session_maker():
            query = select(HotelsOrm)

            if title:
                query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
            if location:
                query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))


            query = query.limit(limit).offset(offset)
            result = await self.session.execute(query)

            return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location, title, limit, offset
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(HotelsOrm.title.ilike(f"%{title}%"))

        hotels_ids_to_get = hotels_ids_to_get.limit(limit).offset(offset)
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))