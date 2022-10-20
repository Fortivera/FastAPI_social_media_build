from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, posts, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


my_posts = [{'title': 'title of post1',
             "content": 'content of post1', 'id': 1}, {'title': "title of post2", 'content': 'content of post2', "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
