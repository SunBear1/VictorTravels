from pydantic import BaseModel


class UserRegisterData(BaseModel):
    email: str
    password: str


class UserUpdateData(BaseModel):
    email: str
    password: str


class UserLoginData(BaseModel):
    email: str
    password: str
