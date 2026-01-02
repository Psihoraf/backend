
from pydantic import BaseModel

class ImageAddIntoBD(BaseModel):
    image_name: str
    image_bites: bytes
class Images(ImageAddIntoBD):
    id: int

class HotelsImagesAdd(BaseModel):
    hotel_id: int
    image_id:int

class HotelsImages(HotelsImagesAdd):
    id:int