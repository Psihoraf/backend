from pydantic import BaseModel, ConfigDict, EmailStr



class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class User(UserModel):
    email: EmailStr
    id:int

class UserRequestAdd(UserModel):
    email: EmailStr
    password: str

class UserAdd(UserModel):
    email:EmailStr
    hashed_password: str