from fastapi import Query, APIRouter, Body
from src.Schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import  PginationDep
from src.database import async_session_maker
from sqlalchemy import insert, select

from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


def pagination(page, per_page, hotels_):
    start = (page - 1) * per_page
    end = start + per_page
    hotels_ = hotels_[start:end]
    return hotels_



@router.get("")
async def get_hotels(
        paginations: PginationDep,

        title: str |None = Query(None, description="Название города"),
        location: str|None = Query(None, description="Адрес отеля")
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location = location,
            title = title,
            limit=paginations.per_page or 5,
            offset=paginations.per_page * (paginations.page - 1)
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id = hotel_id)
    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id:int
):
    async with async_session_maker() as session:
        if not await HotelsRepository(session).check_existence(hotel_id):
            return {"Status": "Error", "Message": "Hotel not found "}

        await HotelsRepository(session).delete(id = hotel_id)
        await session.commit()
    return {"Status":"OK"}

@router.post("")
async def create_hotel(
        data_hotel: HotelAdd = Body(openapi_examples ={
            "1":{"summary": "Сочи", "value":{
                "title":"Delux",
                "location":"Сочи, улица камышевского",
            } },
            "2":{"summary": "Дубай", "value":{
                "title":"Pleasure",
                "location":"улица дубровская",
            }},
            "3":{"summary": "Екатеринбург", "value":{
                "title":"Charm",
                "location":"Екатеринбург, улица золотого сечения 3",
            }}
        })
):
    async with async_session_maker() as session:



        hotel = await HotelsRepository(session).add(data_hotel)

        await session.commit()
    return {"Status":"OK", "data": hotel}

@router.patch("/{hotel_id}")
async def patch_hotel(
        hotel_id:int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, True, id = hotel_id )
        await session.commit()
    return {"Status": "OK"}



@router.put("/{hotel_id}")
async def put_hotel(
        hotel_id:int,
        data_hotel:HotelAdd

):

    async with async_session_maker() as session:

        await HotelsRepository(session).edit(data_hotel, False, id = hotel_id)
        await session.commit()
    return {"Status" : "OK"}