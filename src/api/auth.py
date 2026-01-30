
from fastapi import APIRouter, Response, Request

from src.exceptions import UserAlreadyExistsException, UserWithSuchEmailAlreadyExistsHTTPExceptions, \
    UserNotFoundException, UserNotFoundHTTPException, UserAlreadyLogInHTTPException, UserAlreadyLogInException, \
    UserAlreadyLogOutHTTPException
from src.Schemas.users import UserRequestAdd
from src.api.dependencies import UserIdDep, DBDep

from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(data: UserRequestAdd, db:DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserWithSuchEmailAlreadyExistsHTTPExceptions
    return {f"Пользователь: {data.email} успешно зарегистрирован"}

@router.post("/login")
async def login_user(data: UserRequestAdd, response:Response, db:DBDep, request:Request):
    try:
        request.cookies.get("access_token")
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserAlreadyLogInException:
        raise UserAlreadyLogInHTTPException

    response.set_cookie("access_token", access_token)
    return {"email":data.email, "access_token": access_token}


@router.get("/me")
async def me(user_id:UserIdDep, db:DBDep):
    user = await AuthService(db).get_me(user_id)
    return user

@router.post("/logout")
async def logout_user(response:Response, request:Request):
    if not request.cookies.get("access_token"):
        raise UserAlreadyLogOutHTTPException
    response.delete_cookie("access_token")
    return {"Status":"OK"}
