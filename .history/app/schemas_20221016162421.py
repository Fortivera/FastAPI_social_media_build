from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# ___this is our schema/pydantic model___
# it defines the structure of a request & response
# this insures the user will type exactly whats needed


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# we are using inheritance here so dont have to specify same parameters again


class PostCreate(PostBase):
    pass

# ___________this is schema for receiving data________________


class Post(BaseModel):
    id: int
    created_at: datetime


# we need to do this because pydentic from main.py doesnt know what to do with this sqlalchemy model, it only knows how to
# work with dictionaries

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ShowUser(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
