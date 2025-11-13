from pydantic import BaseModel, ConfigDict


class FacilityModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FacilityAdd(FacilityModel):
    title: str

class Facility(FacilityAdd):
    id:int