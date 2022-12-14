from fastapi import FastAPI
from .routers import users, posts, auth, likes
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) #dont need this if you are using alembic, this autogenerates tables in postgresql

# CORS (Cross-Origin Resource Sharing) specifications
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# homepage call


@app.get('/')
def greeting():

    return {'status': "Add /docs to the end of the current url to access FastAPI testing!"}


# calling the routers for each FastAPI operation, actuall task is written in the routers folder
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
