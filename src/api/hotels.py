from datetime import date
from fastapi_cache.decorator import cache
from fastapi import Query, APIRouter, Body

from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from, HotelExistsExceptionHTTPExceptions, \
    NothingToUpdateExceptionHTTPException
from src.Schemas.hotels import HotelPATCH, HotelAdd


from src.api.dependencies import DBDep, PaginationDep
from src.services.hotels import HotelsService

router = APIRouter(prefix="/hotels", tags=["Отели"])

def pagination(page, per_page, hotels_):
    start = (page - 1) * per_page
    end = start + per_page
    hotels_ = hotels_[start:end]
    return hotels_

@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    return await HotelsService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):

    try:
        hotel = await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelExistsExceptionHTTPExceptions
    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id:int,
        db: DBDep
):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"Status":"OK"}

@router.post("")
async def create_hotel(db: DBDep,

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
    hotel = await HotelsService(db).add_hotel(data_hotel)
    return {"data": hotel}

@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep,
        hotel_id:int,
        hotel_data: HotelPATCH
):
    update_dict = hotel_data.model_dump(exclude_unset=True, exclude_none=True)
    if not update_dict:
        # Ничего не передали для обновления
        raise NothingToUpdateExceptionHTTPException

    await HotelsService(db).edit_hotel_partially(hotel_data,hotel_id, exclude_unset=True)
    return {"Status": "OK"}

@router.put("/{hotel_id}")
async def put_hotel(db: DBDep,
        hotel_id:int,
        data_hotel:HotelAdd

):

    await HotelsService(db).edit_hotel(data_hotel, hotel_id)
    return {"Status" : "OK"}