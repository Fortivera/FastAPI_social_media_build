from argparse import OPTIONAL
from random import randint, randrange
from re import L
from traceback import print_tb
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host='localhost', database='APIdatabase',
                            user='postgres', password='postgres', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
except Exception as error:
    print(f'conn failed, {error}')


my_posts = [{'title': 'title of post1',
             "content": 'content of post1', 'id': 1}, {'title': "title of post2", 'content': 'content of post2', "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post('/posts')
def create_posts(post: Post):
    cursor.execute("""SELECT * FROM posts""")
    new_post = cursor.fetchall()

    return {'data': 'new post'}


@app.get('/posts/{id}')
def get_posts(id):
    post = find_post(int(id))
    print(post)
    return {'post detail': post}
