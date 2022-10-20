from re import L
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "perchik kerchik"}


@app.get('/kek')
def posting():
    return {'message': 'mine'}


@app.get('/createpost')
def creatingpost():
    return {'message': 'create this'}
