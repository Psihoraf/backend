from src.models.images import ImagesOrm, HotelsImagesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ImagesDataMapper, HotelsDataMapperWithImg


class ImagesRepository(BaseRepository):
    mapper = ImagesDataMapper
    model = ImagesOrm

class HotelsImagesRepository(BaseRepository):
    mapper = HotelsDataMapperWithImg
    model = HotelsImagesOrm

