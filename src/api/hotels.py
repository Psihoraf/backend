from fastapi import Query, APIRouter, Body
from src.Schemas.hotels import Hotel,  HotelPATCH
from src.api.dependencies import  PginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

def pagination(page, per_page, hotels_):
    start = (page - 1) * per_page
    end = start + per_page
    hotels_ = hotels_[start:end]
    return hotels_



@router.get("")
def get_hotels(
        paginations: PginationDep,
        id: int |None=Query(None, description="Айдишник"),
        title: str |None = Query(None, description="Название города")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    pagination_hotels = pagination(paginations.page, paginations.per_page, hotels_)
    return pagination_hotels

@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id:int
):
    global hotels
    hotels= [hotel for hotel in hotels if hotel["id"]!=hotel_id]
    return {"status":"OK"}

@router.post("")
def create_hotel(
        data_hotel: Hotel = Body(openapi_examples ={
            "1":{"summary": "Сочи", "value":{
                "title":"Отель у сочи",
                "name":"cool Sochi",
            } },
            "2":{"summary": "Дубай", "value":{
                "title":"Дубай офигенный",
                "name":"cool Dubai",
            }}
        })
):
    global hotels
    hotels.append({
        "id":hotels[-1]["id"]+1,
        "title": data_hotel.title,
        "name": data_hotel.name,
    })
    return {"Status":"OK"}

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