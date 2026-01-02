from fastapi import HTTPException

from sqlalchemy import select

from src.Schemas.facilities import RoomFacility
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilitiesDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper

    async def check_bulk(self, data:list[int]):
        current = (
            select(self.model.id)
        )
        result = await self.session.execute(current)
        current_ids = result.scalars().all()

        current_ids = {f_id for f_id in current_ids}

        new_ids = {f_id for f_id in data}

        incorrect_ids = new_ids-current_ids

        if incorrect_ids:
            raise HTTPException(404, detail=f"удобства с id: {incorrect_ids} не найдены" )

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

