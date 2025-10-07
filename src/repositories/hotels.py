from sqlalchemy import select, insert

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async  def get_all(self, location, title, limit, offset ):

         async with async_session_maker() as session:
            query = select(HotelsOrm)

            if title:
                query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
            if location:
                query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))


            query = query.limit(limit).offset(offset)
            result = await self.session.execute(query)

            return result.scalars().all()

    async def add(self, data_hotel):

        async with async_session_maker() as session:

            add_hotel_stmt = insert(self.model).values(**data_hotel.model_dump()).returning(self.model)
            print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_hotel_stmt)
            return result.scalar_one()




