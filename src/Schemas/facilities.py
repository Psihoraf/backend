from pydantic import BaseModel, ConfigDict, Field


class FacilityModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FacilityAdd(FacilityModel):
    title: str = Field(min_length=1)

class Facility(FacilityAdd):
    id:int

class RoomsFacilitiesAdd(FacilityModel):
    room_id:int
    facility_id:int

class RoomFacility(RoomsFacilitiesAdd):
    id:int