from pydantic import BaseModel

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.Schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User


