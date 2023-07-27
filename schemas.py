from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    phone: str
    password: str

    class Config:
        orm_mode = True
