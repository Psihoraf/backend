from datetime import date

from sqlalchemy import select, func

from src.Schemas.rooms import Rooms, RoomsWithRels

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataMapperWithRels
from src.repositories.utils import rooms_ids_for_booking
from sqlalchemy.orm import selectinload, joinedload

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomDataMapperWithRels.map_to_domain_entity(model) for model in result.unique().scalars().all()]