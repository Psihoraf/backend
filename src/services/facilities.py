from src.Schemas.facilities import RoomsFacilitiesAdd, FacilityAdd
from src.Schemas.rooms import RoomPatchRequest
from src.services.base import BaseService


class FacilitiesService(BaseService):
    async def get_facilities(self):
        return self.db.facilities.get_all()

    async def add_facility(self, data_facility:FacilityAdd):
        await self.db.facilities.add(data_facility)
        await self.db.commit()

    async def add_bulk(self, rooms_facilities_data:list[RoomsFacilitiesAdd]):
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def edit_bulk(self,facilities: list[RoomPatchRequest], room_id:int):
        await self.db.rooms_facilities.edit_bulk(facilities, room_id)
        await self.db.commit()

    async def check_bulk(self,facilities: list[RoomPatchRequest]):
        await self.db.facilities.check_bulk(facilities)
