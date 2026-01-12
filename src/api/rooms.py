from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException


from src.Schemas.facilities import RoomsFacilitiesAdd
from src.api.dependencies import DBDep

from src.Schemas.rooms import RoomsAdd,  RoomPatchRequest, RoomPatch


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/room")
async def get_room(db:DBDep, hotel_id:int, room_id:int ):


        rooms = await db.rooms.get_one_or_none(id=room_id, hotel_id = hotel_id)
        if not rooms:
            return {"status": "Номер не найден"}
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
async def add_room(hotel_id: int, db:DBDep,data_room: RoomPatchRequest = Body(openapi_examples=
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
        hotel_id:int,
        room_id: int,

        data_room: RoomPatchRequest = Body(openapi_examples=
        {
            "1": {"summary": "Королевский", "value": {
                "title": "Королевский",
                "description": "Королевский номер",
                "price": 35000,
                "quantity": 1,
                "facilities_ids": [3]

            }},
        })
):

    _room_data_dict = data_room.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.edit(_room_data, True, id=room_id)

    if "facilities_ids" in _room_data_dict:


        facilities = [f_id for f_id in data_room.facilities_ids]

        await db.facilities.check_bulk(facilities)

        await db.rooms_facilities.edit_bulk(facilities, room_id)
    await db.commit()
    return {"Status": "OK"}

@router.put("/rooms/{room_id}")
async def put_room (db:DBDep,
        hotel_id:int,
        room_id: int,

        data_room: RoomPatchRequest = Body(openapi_examples=
        {
            "1": {"summary": "Королевский", "value": {
                "title": "Арташесовский",
                "description": "Арташесвокий номер",
                "price": 100,
                "quantity": 30,
                "facilities_ids": [1, 3]

            }},
        })
):

    _room_data_dict = data_room.model_dump()
    _room_data = RoomsAdd(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.edit(_room_data, False, id=room_id)

    facilities = [f_id for f_id in data_room.facilities_ids]

    await db.facilities.check_bulk(facilities)

    await db.rooms_facilities.edit_bulk(facilities, room_id)
    await db.commit()
    return {"Status": "OK"}

