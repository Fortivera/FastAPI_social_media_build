
from pydantic import BaseModel
from datetime import datetime

# ___this is our schema/pydantic model___
# it defines the structure of a request & response
# this insures the user will type exactly whats needed


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
# _____________________________________________


class PostCreate(PostBase):
    pass

# ___________this is schema for receiving data________________


class Post(BaseModel):
    id: int
    # title: str
    # content: str
    # published: bool = True
    # created_at: datetime


# we need to do this because pydentic from main.py doesnt know what to do with this sqlalchemy model, it only knows how to
# work with dictionaries

    class Config:
        orm_mode = True
