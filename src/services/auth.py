from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

from src.Schemas.users import UserAdd, UserRequestAdd
from src.config import  settings
import jwt
from passlib.context import CryptContext

from src.exceptions import check_password_validate, ObjectAlreadyExistsException, UserAlreadyExistsException, \
    ObjectNotFoundException, UserNotFoundException, WrongPasswordHTTPException
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password:str):
        check_password_validate(password)
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        ver_password = self.pwd_context.verify(plain_password, hashed_password)
        if not ver_password:
            raise WrongPasswordHTTPException
        return ver_password

    def decode_token(self, token:str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code = 401, detail = "Неверный токен" )

    async def register_user(self, data:UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        await self.db.commit()

    async def login_user(self, data: UserRequestAdd):

        try:
            user = await self.db.users.get_user_with_hashed_password(email=data.email)
        except ObjectNotFoundException:
            raise UserNotFoundException
        self.verify_password(data.password, user.hashed_password)
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_me(self, user_id:int):
        return await self.db.users.get_one(id=user_id)
