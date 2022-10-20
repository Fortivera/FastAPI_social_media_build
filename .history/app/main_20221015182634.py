from argparse import OPTIONAL
from msilib import schema
from multiprocessing import synchronize
from random import randint, randrange
from re import L
from traceback import print_tb
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import get_db, engine
from . import models, schemas
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


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


@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get('/posts/{id}', response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * from posts WHERE id =(%s)""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).all()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with {id}id")
    return post


@ app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # SQL syntax________
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchall()
    # ____________________

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @ app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT, response_model=schemas.Post)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     # cursor.execute(
#     #     """DELETE FROM posts WHERE id = (%s) RETURNING * """, str((id)))
#     # post = cursor.fetchone()
#     # conn.commit()

#     post = db.query(models.Post).filter(models.Post.id == id)

#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f'post with {id}id not found')

#     post.delete(synchronize_session=False)
#     db.commit()

    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id= %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id}id was not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {'data': post_query.first()}


@app.post("/createusers")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
