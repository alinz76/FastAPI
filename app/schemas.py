from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str



class Owner(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    creator_id: int
    owner: Owner

    class Config:
        from_attributes = True




class ReadAllPosts(BaseModel):
    Post: Post
    likes: int



class UserRegister(BaseModel):
    email : EmailStr
    password : str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    email : EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Votes(BaseModel):
    post_id: int
    dir: conint(le=1)