from fastapi import APIRouter, Body

from src.Schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
        db:DBDep
):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(
        db:DBDep,
        data_facility: FacilityAdd = Body(openapi_examples={
            "1": {"summary": "Кондиционер", "value": {
                "title": "Кондиционер",
            }},
            "2": {"summary": "Интернет", "value": {
                "title": "Интернет",
            }},
            "3": {"summary": "Бассейн", "value": {
                "title": "Бассейн",
            }}
        })
):
    await db.facilities.add(data_facility)
    await db.commit()
    return {"Status": "OK" }


