from argparse import OPTIONAL
from random import randint, randrange
from re import L
from traceback import print_tb
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='APIdatabase',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f'conn failed, {error}')
        time.sleep(2)


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
def get_posts(id: int):

    cursor.execute("""SELECT * from posts WHERE id =(%s)""", (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with {id}id")
    return {'post detail': post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()

    return {'data': new_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = (%s) RETURNING * """, str((id)))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {id}id not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def create_posts(post: Post, id: int):
    cursor.execute(
        """UPDATE posts SET title=%s, content=%s published=%s RETURNING * """, (post.title, post.content, post.published))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id}id was not found")

    return {'data': updated_post}
