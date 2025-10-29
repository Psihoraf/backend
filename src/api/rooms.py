from fastapi import APIRouter, Query, Body

from src.Schemas.rooms import Rooms

router = APIRouter(prefix="/hotels", tags=["Номера"])

rooms = [
    {"room_id": 1, "title": "coolRoom", "hotel_id": 13},
    {"room_id": 2, "title": "greatRoom", "hotel_id": 2},
    {"room_id": 3, "title": "badRoom", "hotel_id": 1}
]

@router.get("/{hotel_id}/rooms")
def get_room_of_hotel(hotel_id: int, ):

    #rooms_ = []
    #for room in rooms:
        #if room["hotel_id"] == hotel_id:
            #rooms_.append(room)
    #if not rooms_ :
        #return {"Status":"Номеров, привязанных к этому id нет"}
    #return rooms_


@router.get("/rooms/{room_id}")
def get_all_rooms():

    return rooms

@router.post("/rooms")
def add_room( data_room: Rooms = Body(openapi_examples=
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
    new_id = max(room["room_id"] for room in rooms) + 1 if rooms else 1
    new_room = {
        "room_id":new_id,
        "title":data_room.title,
        "description":data_room.description,
        "price":data_room.price,
        "quantity": data_room.quantity

    }
    rooms.append(new_room)
    return {"Status":"OK"}

@router.delete("/rooms/{room_id}")
def delete_room(room_id:int):

    for room in rooms:
        if room["room_id"] == room_id:
            rooms.remove(room)
            break
    return {"Status": "OK"}

@router.patch("/rooms/{room_id}")
def patch_room(
        room_id: int,
        title:str |None = Body(None),
        hotel_id:int |None = Body(None)
):
    for room in rooms:
        if room["room_id"] == room_id:
            if title:
                room["title"] =title
            if hotel_id:
                room["hotel_id"] = hotel_id
            break
    return {"Status": "OK"}

@router.put("/rooms/{room_id}")
def put_room(room_id: int,
        title:str  = Body(),
        hotel_id:int  = Body()
):
    for room in rooms:
        if room["room_id"] == room_id:
            room["title"] = title
            room["hotel_id"] = hotel_id
        break
    return {"Status": "OK"}


