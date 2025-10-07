from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs) :
        query = select(self.model)
        result = await self.session.execute(query)
        return  result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_ore_none()

    async def add(self, data_hotel):

            add_hotel_stmt = insert(self.model).values(**data_hotel.model_dump()).returning(self.model)
            print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_hotel_stmt)
            return result.scalar_one()

    async def delete(self, hotel_id):
        query = delete(self.model).where(self.model.id == hotel_id)
        await self.session.execute(query)

    async def edit(self, data: BaseModel, hotel_id):

        query = (
    update(self.model)
    .where(self.model.id == hotel_id)
    .values(**data.model_dump())
    .returning(self.model)
    )
        await self.session.execute(query)





