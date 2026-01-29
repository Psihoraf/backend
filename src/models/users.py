from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column


from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)

