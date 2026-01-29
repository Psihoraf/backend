from datetime import date

from fastapi import APIRouter, Query, Body

from src.exceptions import ObjectNotFoundException, \
    HotelExistsExceptionHTTPExceptions, RoomExistsExceptionHTTPExceptions, RoomsExistsExceptionHTTPExceptions

from src.api.dependencies import DBDep

from src.Schemas.rooms import   RoomPatchRequest

from src.services.hotels import HotelsService
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/room")
async def get_room(db:DBDep, hotel_id:int, room_id:int ):

    try:
        room = await RoomsService(db).get_room(hotel_id, room_id)
        return room
    except ObjectNotFoundException:
        raise RoomExistsExceptionHTTPExceptions


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    rooms = await RoomsService(db).get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    if not rooms:
        raise RoomsExistsExceptionHTTPExceptions
    return rooms

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
            "facilities_ids": [1, 3]
        }},
    })
              ):
    try:
        await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelExistsExceptionHTTPExceptions

    room = await RoomsService(db).add_room(hotel_id,data_room)

    return {"room":room}

@router.delete("/rooms/{room_id}")
async def delete_room(hotel_id:int, room_id:int, db:DBDep):
    try:
        await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelExistsExceptionHTTPExceptions
    try:
        await RoomsService(db).get_room(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomExistsExceptionHTTPExceptions

    await RoomsService(db).delete_room(hotel_id, room_id )
    return {"Status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
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
    try:
        await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelExistsExceptionHTTPExceptions
    try:
        await RoomsService(db).get_room(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomExistsExceptionHTTPExceptions


    await RoomsService(db).edit_room_partially(data_room, room_id,hotel_id, exclude_unset = True)
    return {"Status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room (db:DBDep,
        hotel_id:int,
        room_id: int,

        data_room: RoomPatchRequest = Body(openapi_examples=
        {
            "1": {"summary": "Королевский", "value": {
                "title": "Королевский",
                "description": "Королевский номер",
                "price": 100,
                "quantity": 30,
                "facilities_ids": [1, 3]
            }},
        })
):
    try:
        await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelExistsExceptionHTTPExceptions
    try:
        await RoomsService(db).get_room(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomExistsExceptionHTTPExceptions

    await RoomsService(db).edit_room(data_room, room_id, hotel_id)
    return {"Status": "OK"}

