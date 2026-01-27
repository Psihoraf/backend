from pydantic import  EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.exceptions import ObjectNotFoundException
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.Schemas.users import User, UserWithHashedPassword
from src.repositories.mappers.mappers import UserDataMapper


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email:EmailStr):
        query = select(self.model).filter_by(email = email)
        result = await self.session.execute(query)

        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return UserWithHashedPassword.model_validate(model)

    async def get_user(self, email:EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return User.model_validate(model)

