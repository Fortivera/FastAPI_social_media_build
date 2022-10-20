from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from .. import models, schemas, utils, database
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
