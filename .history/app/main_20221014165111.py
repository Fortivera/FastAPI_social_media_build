from argparse import OPTIONAL
from http.client import HTTPException
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


@app.get('/posts/{id}')
def get_posts(id):

    cursor.execute("""SELECT * from posts WHERE id =(%s)""", (id))
    post = cursor.fetchone()
    print(post)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post not found with {id}id")
    return {'post detail': post}


@app.post('/posts')
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()

    return {'data': new_post}
