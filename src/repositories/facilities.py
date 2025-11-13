from src.Schemas.facilities import Facility
from src.models.facilities import FacilitiesORM
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility