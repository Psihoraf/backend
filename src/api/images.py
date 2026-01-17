import shutil


from fastapi import APIRouter, UploadFile


from src.Schemas.images import ImageAddIntoBD, HotelsImagesAdd
from src.api.dependencies import DBDep
from src.services.images import ImagesService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images",tags=["Изображения отелей"] )

@router.post("")
async def upload_files(db: DBDep,
                       file: UploadFile,
                       image_name:str|None,
                       hotel_id:int
                       ):
    await ImagesService(db).add_image(file, image_name,hotel_id)
    return {"Status": "OK"}


    #загрузить картинку

    #отправить в бд