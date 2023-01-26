from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserDelete(BaseModel):
    id: int


class UserDeleteResponse(UserDelete):
    deleted: bool
    detail: dict | None
