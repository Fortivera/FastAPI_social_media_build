from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, posts, auth, likes
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) #dont need this if you are using alembic, this autogenerates tables in postgresql

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def greeting():

    return {'status': "you have reched main.py"}


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
