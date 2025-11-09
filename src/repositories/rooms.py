from sqlalchemy import select

from src.Schemas.rooms import  RoomsResponse

from src.database import async_session_maker
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository




class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomsResponse

    async def get_room_of_hotel_id(self, **filter_by):

        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        return  [self.schema.model_validate(model) for model in result.scalars().all()]

