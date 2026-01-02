from src.Schemas.bookings import Booking
from src.Schemas.facilities import Facility
from src.Schemas.hotels import Hotel
from src.Schemas.images import Images, HotelsImagesAdd
from src.Schemas.rooms import Rooms, RoomsWithRels
from src.Schemas.users import User
from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.images import ImagesOrm, HotelsImagesOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper


class HotelDataMapper(DataMapper):
    model = HotelsOrm
    schema = Hotel

class RoomDataMapper(DataMapper):
    model = RoomsOrm
    schema = Rooms

class RoomDataMapperWithRels(DataMapper):
    model = RoomsOrm
    schema = RoomsWithRels

class UserDataMapper(DataMapper):
    model = UsersOrm
    schema = User

class BookingDataMapper(DataMapper):
    model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    model = FacilitiesOrm
    schema = Facility

class ImagesDataMapper(DataMapper):
    model = ImagesOrm
    schema = Images

class HotelsDataMapperWithImg(DataMapper):
    model = HotelsImagesOrm
    schema = HotelsImagesAdd



