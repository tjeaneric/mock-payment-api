import uuid as uuid_pkg
from sqlmodel import SQLModel, Field
from typing import Union


class UserBase(SQLModel):
    username: str = Field(nullable=False)
    phone: str = Field(nullable=False)


class UserLogin(SQLModel):
    phone: str
    password: str


class User(UserBase, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, nullable=False)
    password: str = Field(nullable=False)


class UserCreate(UserBase):
    password: str = Field(nullable=False, max_length=4, min_length=4)


class UserUpdate(SQLModel):
    username: Union[str, None] = None
    phone: Union[str, None] = None
    password: Union[str, None] = None


class ResponseBase(UserBase):
    id: uuid_pkg.UUID


class TokenBase(SQLModel):
    access_token: str
    token_type: str
    data: ResponseBase

