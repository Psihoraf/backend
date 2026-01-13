from datetime import date

from fastapi import HTTPException


class MegaBroniratorExceptions(Exception):

    detail = "Очень неожиданная ошибочка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundException(MegaBroniratorExceptions):

    detail = "Объект не найден"

class ObjectAlreadyExistsException(MegaBroniratorExceptions):
    detail = "Пользователь уже существует "

class AllRoomsAlreadyHaveBooked(MegaBroniratorExceptions):
    detail = "Нет свободных номеров"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")

class DateFromSoonerThenDateToException(MegaBroniratorExceptions):
    detail = "Дата выезда позже, чем дата заезда"


class MegaBroniratorHTTPExceptions(HTTPException):
    status_code = 500
    detail = None
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelExistsException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Такой отель не существует"

class RoomExistsException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Такой номер не существует"

class UserWithSuchEmailAlreadyExists(MegaBroniratorHTTPExceptions):
    status_code = 400
    detail = "Пользователь уже существует "