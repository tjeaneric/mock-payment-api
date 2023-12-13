import uuid as uuid_pkg
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import field_validator


class UserBase(SQLModel):
    first_name: str
    last_name: str
    phone: str

    @field_validator('phone')
    def validate_phone(cls, value):
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        return value


class User(UserBase, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)


class UserCreate(UserBase):
    password: str = Field(max_length=4, min_length=4)


class UserUpdate(SQLModel):
    username: str | None
    phone: str | None
    password: str | None


class ResponseBase(UserBase):
    id: uuid_pkg.UUID
    created_at: datetime


class TokenBase(SQLModel):
    access_token: str
    token_type: str
    data: ResponseBase


# Models for transaction Table

class TransactionBase(SQLModel):
    sender_phone: str = Field(foreign_key="user.phone")
    receiver_phone: str = Field(nullable=False)
    product: str = Field(nullable=False)
    amount: int = Field(nullable=False)


class Transaction(TransactionBase, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, nullable=False)
    deleted_status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)


class TransactionRequest(TransactionBase):
    pass
