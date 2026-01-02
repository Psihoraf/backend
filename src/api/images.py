import shutil


from fastapi import APIRouter, UploadFile, Query

from src.Schemas.images import  ImageAddIntoBD
from src.api.dependencies import DBDep
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images",tags=["Изображения отелей"] )

@router.post("")
async def upload_files(db: DBDep,
                       file: UploadFile,
                       image_name:str|None = Query(None)
                       ):
    image_path = f"src/static/images/{file.filename}"

    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image.delay(image_path)

    with open(image_path, "rb") as read_binary:
        image_data = read_binary.read()

    query = ImageAddIntoBD(image_name=image_name, image_bites=image_data)
    await db.images.add(query)

    await db.commit()
    return {"Status": "OK"}


    #загрузить картинку

    #отправить в бд