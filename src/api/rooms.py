from fastapi import APIRouter, Query, Body, HTTPException

from src.models.hotels import HotelsOrm
from src.Schemas.rooms import RoomsAdd, RoomsResponse
from src.database import async_session_maker

from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Номера"])

rooms = [
    {"room_id": 1, "title": "coolRoom", "hotel_id": 13},
    {"room_id": 2, "title": "greatRoom", "hotel_id": 2},
    {"room_id": 3, "title": "badRoom", "hotel_id": 1}
]


@router.get("/rooms/all")
async def get_all_rooms():
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all()
        if not rooms:
            return {"status": "Номера не найдены"}
        return rooms

@router.get("/{hotel_id}/rooms")
async def get_room_of_hotel(hotel_id:int):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_room_of_hotel_id(hotel_id = hotel_id)
        if not rooms:
            return {"Status": "Номер не найден"}
        return rooms

@router.post("/rooms")
async def add_room( data_room: RoomsAdd = Body(openapi_examples=
    {
        "1": {"summary": "Крутой", "value": {
            "hotel_id":1,
            "title": "ВИП1",
            "description": "Самый лучший номер",
            "price":2000,
            "quantity":12,

        }},
        "2": {"summary": "Нормальный", "value": {
            "hotel_id":13,
            "title": "Дефолт",
            "description": "Обычный номер",
            "price":1000,
            "quantity":30,

        }},
        "3": {"summary": "Дешевый", "value": {
            "hotel_id":2,
            "title": "Бедный",
            "description": "Самый дешевый номер",
            "price":500,
            "quantity":23,


        }},
    })

              ):
    async with async_session_maker() as session:
        hotel = await session.get(HotelsOrm, data_room.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        await RoomsRepository(session).add(data_room)
        await session.commit()

    return {"Status":"OK"}

@router.delete("/rooms/{room_id}")
async def delete_room(room_id:int):

    async with async_session_maker() as session:
        room = await RoomsRepository(session).delete(id = room_id )
        if not room:
            raise HTTPException(status_code=404, detail="Hotel not found")
        await session.commit()
    return {"Status": "OK"}

@router.patch("/rooms/{room_id}")
async def patch_room(
        room_id: int,
        data_room: RoomsAdd = Body(openapi_examples=
        {
            "1": {"summary": "Королевский", "value": {
                "hotel_id": 17,
                "title": "Королевский",
                "description": "Королевский номер",
                "price": 35000,
                "quantity": 1,

            }},
        })
):
    async with async_session_maker() as session:
        hotel = await session.get(HotelsOrm, data_room.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        await RoomsRepository(session).edit(data_room, False, id=room_id)
        await session.commit()
    return {"Status": "OK"}

@router.put("/rooms/{room_id}")
async def put_room(room_id: int, data_room:RoomsAdd = Body(openapi_examples=
    {
        "1": {"summary": "Царский", "value": {
            "hotel_id":18,
            "title": "Царский",
            "description": "Царский номер",
            "price":10000,
            "quantity":2,

        }},
    })
                   ):

    async with async_session_maker() as session:
        hotel = await session.get(HotelsOrm, data_room.hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        await RoomsRepository(session).edit(data_room, False, id = room_id)
        await session.commit()

    return {"Status": "OK"}


