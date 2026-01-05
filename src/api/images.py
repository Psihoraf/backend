import shutil


from fastapi import APIRouter, UploadFile, Query
from sqlalchemy import text

from src.Schemas.images import ImageAddIntoBD, HotelsImagesAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images",tags=["Изображения отелей"] )

@router.post("")
async def upload_files(db: DBDep,
                       file: UploadFile,
                       image_name:str|None,
                       hotel_id:int
                       ):
    image_path = f"src/static/images/{file.filename}"

    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)

    with open(image_path, "rb") as read_binary:
        image_bites = read_binary.read()





    data_image = ImageAddIntoBD(image_name=image_name, image_bites=image_bites)
    image = await db.images.add(data_image)


    hotel_image = HotelsImagesAdd(hotel_id=hotel_id, image_id=image.id)
    await db.hotels_images.add(hotel_image)


    await db.commit()
    return {"Status": "OK"}


    #загрузить картинку

    #отправить в бд