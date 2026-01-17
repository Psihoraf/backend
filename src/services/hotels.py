from datetime import date

from src.Schemas.hotels import HotelAdd, HotelPATCH
from src.exceptions import check_date_to_after_date_from
from src.services.base import BaseService


class HotelsService(BaseService):

    async def get_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date
    ):
        per_page = pagination.per_page or 5
        check_date_to_after_date_from(date_from, date_to)

        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

    async def get_hotel(self, hotel_id:int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def delete_hotel(self, hotel_id:int):
        hotel = await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        return hotel

    async def add_hotel(self, data_hotel:HotelAdd):
        await self.db.hotels.add(data_hotel)
        await self.db.commit()

    async def edit_hotel(self,hotel_data:HotelAdd,hotel_id:int):
        await self.db.hotels.edit(hotel_data,id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_data:HotelPATCH,hotel_id:int, exclude_unset: bool = False):
        await self.db.hotels.edit(hotel_data,exclude_unset, id=hotel_id)
        await self.db.commit()