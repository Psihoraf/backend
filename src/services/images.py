import shutil

from fastapi import UploadFile

from src.Schemas.images import ImageAddIntoBD, HotelsImagesAdd
from src.services.base import BaseService
from src.tasks.tasks import resize_image

class ImagesService(BaseService):
    async def add_image(self, file: UploadFile,
                       image_name:str|None,
                       hotel_id:int):

        image_path = f"src/static/images/{file.filename}"

        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(image_path)

        with open(image_path, "rb") as read_binary:
            image_bites = read_binary.read()

        data_image = ImageAddIntoBD(image_name=image_name, image_bites=image_bites)
        image = await self.db.images.add(data_image)

        hotel_image = HotelsImagesAdd(hotel_id=hotel_id, image_id=image.id)
        await self.db.hotels_images.add(hotel_image)

        await self.db.commit()

    async def add_image_with_hotel(self,hotel_image: HotelsImagesAdd):
        await self.db.hotels_images.add(hotel_image)
        await self.db.commit()
