from datetime import date

from src.Schemas.facilities import RoomsFacilitiesAdd
from src.Schemas.rooms import RoomsAdd, RoomPatch, RoomPatchRequest
from src.exceptions import check_date_to_after_date_from
from src.services.base import BaseService


class RoomsService(BaseService):
    async def get_room(self, hotel_id:int, room_id:int):
       return await self.db.rooms.get_one_with_facilities(hotel_id=hotel_id, id=room_id)

    async def get_room_for_booking(self, room_id:int):
       return await self.db.rooms.get_one(id=room_id)

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def add_room(self, hotel_id: int, data_room:RoomPatchRequest):

        data_room_ = RoomsAdd(hotel_id=hotel_id, **data_room.model_dump())
        room = await self.db.rooms.add(data_room_)


        rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in
                                 data_room.facilities_ids]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def delete_room(self,hotel_id:int,room_id:int ):
        await self.db.rooms.delete(hotel_id, room_id)
        await self.db.commit()

    async def edit_room_partially(self, data_room:RoomPatchRequest, room_id:int, hotel_id:int, exclude_unset: bool = False):

        _room_data_dict = data_room.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

        await self.db.rooms.edit(_room_data, exclude_unset, id=room_id)

        if "facilities_ids" in _room_data_dict:
            facilities = [f_id for f_id in data_room.facilities_ids]
            await self.db.facilities.check_bulk(facilities)
            await self.db.rooms_facilities.edit_bulk(facilities, room_id)

        await self.db.commit()

    async def edit_room(self, data_room:RoomPatchRequest, room_id:int, hotel_id:int,):
        _room_data_dict = data_room.model_dump()
        _room_data = RoomsAdd(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data,id=room_id)

        facilities = [f_id for f_id in data_room.facilities_ids]
        await self.db.facilities.check_bulk(facilities)
        await self.db.rooms_facilities.edit_bulk(facilities, room_id)
        await self.db.commit()
