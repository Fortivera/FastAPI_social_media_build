from argparse import OPTIONAL
from random import randint, randrange
from re import L
from traceback import print_tb
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "perchik kerchik"}


@app.get('/')
def posting():
    return {'message': 'mine'}


@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000)
    return {'data': 'new post'}


@app.get('/posts{id}')
def get_posts():
