from fastapi import Query, APIRouter, Body
from src.Schemas.hotels import Hotel,  HotelPATCH
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


@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id:int
):
    global hotels
    hotels= [hotel for hotel in hotels if hotel["id"]!=hotel_id]
    return {"status":"OK"}

@router.post("")
async def create_hotel(
        data_hotel: Hotel = Body(openapi_examples ={
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
        repo = HotelsRepository(session)


        hotel = await repo.add(data_hotel)

        await session.commit()
    return {"Status":"OK", "data": hotel}

@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id:int,
        hotel_patch: HotelPATCH
):

    for hotel in hotels:
        if hotel_id and hotel["id"] == hotel_id:
            if hotel_patch.title is not None:
                hotel["title"] = hotel_patch.title
            if hotel_patch.name is not None:
                hotel["name"] = hotel_patch.name
            return hotel


@router.put("/{hotel_id}")
def put_hotel(
        hotel_id:int,
        data_hotel:Hotel

):

    for hotel in hotels:
        if hotel_id and hotel["id"] == hotel_id:
            if data_hotel.title and data_hotel.name is not None:
                hotel["title"] = data_hotel.title
                hotel["name"] = data_hotel.name
                return hotel