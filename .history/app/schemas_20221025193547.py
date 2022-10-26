from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# these are schemas/pydantic models
# they define the structure of request & response 
# this insures the user will type exactly whats needed, and the return is structured 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# we are using inheritance here so we dont specify same parameters again
class PostCreate(PostBase):
    pass

# this is schema for the user related operations
class ShowUser(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

# this is schema for the post related operations
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: ShowUser
# we need to do this because pydentic from main.py doesnt know what to do with this sqlalchemy model, it only knows how to
# work with dictionaries
    class Config:
        orm_mode = True

# schema for creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#shema for loging in a user
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#schema for a token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Like(BaseModel):
    post_id: int
    # 1 is an action to like, 0 is an action to unlike
    like_status: conint(le=1)


class PostBack(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True
