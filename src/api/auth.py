
from fastapi import APIRouter, Response, Request, Body

from src.exceptions import UserAlreadyExistsException, UserWithSuchEmailAlreadyExistsHTTPExceptions, \
    UserNotFoundException, UserNotFoundHTTPException, UserAlreadyLogInHTTPException, UserAlreadyLogInException, \
    UserAlreadyLogOutHTTPException
from src.Schemas.users import UserRequestAdd
from src.api.dependencies import UserIdDep, DBDep

from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(db:DBDep, data: UserRequestAdd = Body(openapi_examples ={
            "1":{"summary": "User1", "value":{
                "email":"user@example.com",
                "password":"QQqq11**",
            } },
            "2":{"summary": "User2", "value":{
                "title":"user2@example.com",
                "location":"PPpp22$$",
            }},
        })):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserWithSuchEmailAlreadyExistsHTTPExceptions
    return {f"Пользователь: {data.email} успешно зарегистрирован"}

@router.post("/login")
async def login_user(response:Response, db:DBDep, request:Request, data: UserRequestAdd= Body(openapi_examples ={
            "1":{"summary": "User1", "value":{
                "email":"user@example.com",
                "password":"QQqq11**",
            } },
            "2":{"summary": "User2", "value":{
                "title":"user2@example.com",
                "location":"PPpp22$$",
            }},
        })):
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
