from fastapi import APIRouter, Body

from src.Schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import task_test
router = APIRouter(prefix="/facilities", tags=["Удобства"])
from fastapi_cache.decorator import cache

@router.get("")
@cache(expire=10)
async def get_facilities(
        db:DBDep
):
    print ("иду в бд")
    return  await db.facilities.get_all()



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

    await db.facilities.add(data_facility)
    await db.commit()
    return {"Status": "OK" }


