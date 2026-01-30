
from pydantic import BaseModel, Field


class ImageAddIntoBD(BaseModel):
    image_name: str = Field(min_length=1)
    image_bites: bytes
class Images(ImageAddIntoBD):
    id: int

class HotelsImagesAdd(BaseModel):
    hotel_id: int
    image_id:int

class HotelsImages(HotelsImagesAdd):
    id:int