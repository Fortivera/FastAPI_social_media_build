from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "perchik kerchik"}


@app.get('/kek')
def posting():
    return {'message': 'mine'}
