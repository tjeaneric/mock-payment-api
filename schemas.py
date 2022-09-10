from pydantic import BaseModel


class userBase(BaseModel):
    username: str
    phone: str
    password: str

    class Config:
        orm_mode = True


# class userResponse(BaseModel):
#     id: str
#     username: str
#     phone: str
