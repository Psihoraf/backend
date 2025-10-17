from sqlalchemy import exists

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

from src.database import async_session_maker


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs) :
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data:BaseModel):

        add_hotel_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_hotel_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)


    async def delete(self, hotel_id):
        query = delete(self.model).where(self.model.id == hotel_id)
        await self.session.execute(query)


    async def edit(self, data: BaseModel, isPatch: bool = False, **filter_by):

        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=isPatch))
            .returning(self.model)
    )
        await self.session.execute(query)


    async def check_existence(self, hotel_id):
        query = select(exists().where(self.model.id == hotel_id))
        result = await self.session.execute(query)
        return result.scalar_one()




