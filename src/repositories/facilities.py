from src.Schemas.facilities import Facility, RoomFacility
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility