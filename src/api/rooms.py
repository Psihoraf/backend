from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from src.Schemas.facilities import RoomsFacilitiesAdd
from src.api.dependencies import DBDep
from src.models.hotels import HotelsOrm
from src.Schemas.rooms import RoomsAdd, RoomsResponse, RoomsAddRequest, RoomsPATCH
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
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.post("/rooms")
async def add_room(hotel_id: int, db:DBDep,data_room: RoomsAddRequest = Body(openapi_examples=
    {
        "1": {"summary": "Крутой", "value": {

            "title": "ВИП1",
            "description": "Самый лучший номер",
            "price":2000,
            "quantity":12,

        }},
        "2": {"summary": "Нормальный", "value": {

            "title": "Дефолт",
            "description": "Обычный номер",
            "price":1000,
            "quantity":30,

        }},
        "3": {"summary": "Дешевый", "value": {

            "title": "Бедный",
            "description": "Самый дешевый номер",
            "price":500,
            "quantity":23,


        }},
    })

              ):

    data_room_ = RoomsAdd(hotel_id=hotel_id, **data_room.model_dump())

    room = await db.rooms.add(data_room_)

    rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in data_room.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
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
        data_room: RoomsPATCH = Body(openapi_examples=
        {
            "1": {"summary": "Королевский", "value": {
                "hotel_id": 17,
                "title": "Королевский",
                "description": "Королевский номер",
                "price": 35000,
                "quantity": 1,
                "facilities_ids": [3]

            }},
        })
):
    data_room_ = RoomsAdd(**data_room.model_dump())

    await db.rooms.edit(data_room_, True, id=room_id)

    rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room_id, facility_id=f_id) for f_id in data_room.facilities_ids]

    await db.rooms_facilities.edit_bulk(rooms_facilities_data, room_id=room_id)
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


