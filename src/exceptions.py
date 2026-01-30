import re
from datetime import date

from fastapi import HTTPException


class MegaBroniratorExceptions(Exception):

    detail = "Очень неожиданная ошибочка"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MegaBroniratorExceptions):
    detail = "Объект не найден"


class UserNotFoundException(MegaBroniratorExceptions):
    detail = "Пользователь не найден"


class UserAlreadyLogInException(MegaBroniratorExceptions):
    detail = "Пользователь уже авторизован"


class UserAlreadyExistsException(MegaBroniratorExceptions):

    detail = "Пользователь уже существует"

class ObjectAlreadyExistsException(MegaBroniratorExceptions):
    detail = "нет "


class AllRoomsAlreadyHaveBookedException(MegaBroniratorExceptions):
    detail = "Нет свободных номеров"

class FacilitiesNotFoundExceptionException(MegaBroniratorExceptions):
    status_code = 404
    detail = "Одно или несколько удобств не найдены"


class DateFromSoonerThenDateToException(MegaBroniratorExceptions):
    detail = "Дата выезда позже, чем дата заезда"

class HotelAlreadyExistsException(MegaBroniratorExceptions):
    detail = "Отель с таким и адресом уже существует"
def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда или равна ей")


pattern = r'^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-zА-Яа-я\d@$!%*#?&_]{8,}$'
def check_password_validate(password:str):
    if re.match(pattern, password) is None:
        raise HTTPException(status_code=401, detail="Пароль должен быть не меньше 8 символов, "
                                                    "иметь буквы верхнего и "
                                                    "нижнего регистра, иметь хотя бы одну цифру, "
                                                    "а также один или более из специальных "
                                                    "символов(@$!%*#?&_)")


class MegaBroniratorHTTPExceptions(HTTPException):
    status_code = 404
    detail = None
    def __init__(self, detail: str = None, *args, **kwargs):
        detail = detail or self.detail
        super().__init__(status_code=self.status_code, detail=detail)


class HotelExistsExceptionHTTPExceptions(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Такой отель не существует"

class HotelAlreadyExistsExceptionHTTPExceptions(MegaBroniratorHTTPExceptions):
    status_code = 409
    detail = "Отель с таким адресом уже существует"

class FacilitiesNotFoundExceptionHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Одно или несколько удобств не найдены"




class RoomExistsExceptionHTTPExceptions(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Такой номер не существует"

class RoomsExistsExceptionHTTPExceptions(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Номера не найдены"


class UserWithSuchEmailAlreadyExistsHTTPExceptions(MegaBroniratorHTTPExceptions):
    status_code = 409
    detail = "Пользователь уже существует!"


class UserNotFoundHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Пользователь не найден!"


class WrongPasswordHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 401
    detail = "Пароль не верный"


class UserAlreadyLogInHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 400
    detail = "Вы уже авторизованы"


class UserAlreadyLogOutHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 400
    detail = "Вы уже вышли из аккаунта"

class AllRoomsAlreadyHaveBookedHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 409
    detail = "Нет свободных номеров"

class BookingNotFoundHTTPEException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Бронирования не найдены, скорее всего их нет"

class FacilitiesNotFoundHTTPEException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Удобства не найдены, скорее всего их нет"

class FacilitiesAlreadyExistsHTTPEException(MegaBroniratorHTTPExceptions):
    status_code = 409
    detail = "Удобство уже существует"

class NothingToUpdateExceptionHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 422
    detail = "Не передано данных для обновления"

