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


class AllRoomsAlreadyHaveBooked(MegaBroniratorExceptions):
    detail = "Нет свободных номеров"


class DateFromSoonerThenDateToException(MegaBroniratorExceptions):
    detail = "Дата выезда позже, чем дата заезда"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


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
    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelExistsException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Такой отель не существует"


class RoomExistsException(MegaBroniratorHTTPExceptions):
    status_code = 404
    detail = "Такой номер не существует"


class UserWithSuchEmailAlreadyExistsHTTPExceptions(MegaBroniratorHTTPExceptions):
    status_code = 400
    detail = "Пользователь уже существует!"


class UserNotFoundHTTPException(MegaBroniratorHTTPExceptions):
    status_code = 401
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

