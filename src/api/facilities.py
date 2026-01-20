from fastapi import APIRouter, Body

from src.Schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep
from src.services.facilities import FacilitiesService
from src.tasks.tasks import task_test
router = APIRouter(prefix="/facilities", tags=["Удобства"])
from fastapi_cache.decorator import cache # noqa:E402

@router.get("")
@cache(expire=10)
async def get_facilities(
        db:DBDep
):
    print ("иду в бд")
    return await FacilitiesService(db).get_facilities()

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
    task_test.delay()
    facility = await FacilitiesService(db).add_facility(data_facility)

    return {"Status": "OK", "data": facility }


