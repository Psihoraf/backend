import logging

from asyncpg import UniqueViolationError

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import joinedload

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.Schemas.rooms import RoomsWithRels
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None

    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs) :
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_or_none(self, *filters, **filter_by ):
        query = (select(self.model)
                 .filter(*filters)
                .filter_by(**filter_by))

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def get_one_with_facilities(self,*filters, **filter_by ):
        query = (select(self.model)
                 .options(joinedload(self.model.facilities))
                 .filter(*filters)
                 .filter_by(**filter_by))
        result = self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return RoomsWithRels.model_validate(model)


    async def get_one_or_none_with_facilities(self, *filters, **filter_by ):
        query = (select(self.model)
                .options(joinedload(self.model.facilities))
                 .filter(*filters)
                .filter_by(**filter_by))

        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None
        return RoomsWithRels.model_validate(model)

    async def get_one_or_none_image(self, *filters, **filter_by ):
        query = (select(self.model)
                 .filter(*filters)
                .filter_by(**filter_by))

        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()

        return self.mapper.map_to_domain_entity(model)
    async def add(self, data:BaseModel):


        #print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        try:
            add_hotel_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_hotel_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            print(f"{type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.exception(
                    f"Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}"
                )
                raise ex



    async def add_image(self, data:BaseModel):
        add_img_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        await self.session.execute(add_img_stmt)

    async def add_bulk(self, data: list[BaseModel]):
        add_hotel_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_hotel_stmt)


    async def edit_bulk(self, facilities_ids: list[int], room_id:int):

        get_current_facilities_ids = (
            select(self.model.facility_id).filter_by(room_id=room_id)
        )
        result = await self.session.execute(get_current_facilities_ids)
        current_facilities_ids = result.scalars().all()



        to_delete_ids : list[int] =list(set(current_facilities_ids)-set(facilities_ids))
        to_add_ids : list[int] =list(set(facilities_ids)-set( current_facilities_ids))

        if to_delete_ids:
            delete_stmt=(
                delete(self.model)
                .filter_by(room_id = room_id)
                .where(
                    self.model.facility_id.in_(to_delete_ids)
                )
            )
            await self.session.execute(delete_stmt)
        if to_add_ids:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in to_add_ids])
            )
            await self.session.execute(insert_m2m_facilities_stmt)






    async def delete(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)


    async def edit(self, data: BaseModel, isPatch: bool = False, **filter_by):

        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=isPatch))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        return self.mapper.map_to_domain_entity(model)

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]


    async def check_existence(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        if not query:
            return False
            #raise HTTPException(status_code=404, detail="Not found")
        return True



