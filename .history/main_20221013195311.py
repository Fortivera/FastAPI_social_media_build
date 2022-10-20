from argparse import OPTIONAL
from re import L
from traceback import print_tb
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool
    rating: Optional[int] = none


@app.get("/")
async def root():
    return {"message": "perchik kerchik"}


@app.get('/kek')
def posting():
    return {'message': 'mine'}


@app.post('/createpost')
def creatingpost(new_post: Post):
    print(new_post.published)
    return {'data': 'new post'}
