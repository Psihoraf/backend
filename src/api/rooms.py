from fastapi import APIRouter, Query, Body, HTTPException

from src.api.dependencies import DBDep
from src.models.hotels import HotelsOrm
from src.Schemas.rooms import RoomsAdd, RoomsResponse
from src.database import async_session_maker

from src.repositories.rooms import RoomsRepository
from src.utils.db_manager import DBManager

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/rooms/all")
async def get_all_rooms(db:DBDep):

        rooms = await db.rooms.get_all()
        if not rooms:
            return {"status": "Номера не найдены"}
        return rooms

@router.get("/{hotel_id}/rooms")
async def get_room_of_hotel(hotel_id:int, db:DBDep):

        rooms = await db.rooms.get_room_of_hotel_id(hotel_id = hotel_id)
        if not rooms:
            return {"Status": "Номер не найден"}
        return rooms

@router.post("/rooms")
async def add_room( db:DBDep,data_room: RoomsAdd = Body(openapi_examples=
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

    hotel = await db.get(HotelsOrm, data_room.hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await db.rooms.add(data_room)
    await db.commit()

    return {"Status":"OK"}

@router.delete("/rooms/{room_id}")
async def delete_room(room_id:int, db:DBDep):


    room = await db.rooms.delete(id = room_id )
    if not room:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await db.commit()
    return {"Status": "OK"}

@router.patch("/rooms/{room_id}")
async def patch_room(
        db:DBDep,
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

    hotel = await db.get(HotelsOrm, data_room.hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await db.rooms.edit(data_room, False, id=room_id)
    await db.commit()
    return {"Status": "OK"}

@router.put("/rooms/{room_id}")
async def put_room(db:DBDep,room_id: int, data_room:RoomsAdd = Body(openapi_examples=
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


    hotel = await db.get(HotelsOrm, data_room.hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    await db.rooms.edit(data_room, False, id = room_id)
    await db.commit()

    return {"Status": "OK"}


