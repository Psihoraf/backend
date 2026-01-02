from datetime import date
from fastapi_cache.decorator import cache
from fastapi import Query, APIRouter, Body
from src.Schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.Schemas.images import HotelsImagesAdd
from src.api.dependencies import  DBDep, PaginationDep

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
    print("иду в бд")
    per_page = pagination.per_page or 5
    #
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):

    hotel = await db.hotels.get_one_or_none(id = hotel_id)
    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id:int,
        db: DBDep
):

    if not await db.hotels.check_existence(hotel_id):
        return {"Status": "Error", "Message": "Hotel not found "}

    await db.hotels.delete(id = hotel_id)
    await db.commit()
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




    hotel = await db.hotels.add(data_hotel)

    await db.commit()
    return {"Status":"OK", "data": hotel}

@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep,
        hotel_id:int,
        hotel_data: HotelPATCH
):

    await db.hotels.edit(hotel_data, True, id = hotel_id )
    await db.commit()
    return {"Status": "OK"}



@router.put("/{hotel_id}")
async def put_hotel(db: DBDep,
        hotel_id:int,
        data_hotel:HotelAdd

):

    await db.hotels.edit(data_hotel, False, id = hotel_id)
    await db.commit()
    return {"Status" : "OK"}