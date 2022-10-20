from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from .. import oauth2

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/APIdatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='APIdatabase',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f'conn failed, {error}')
        time.sleep(2)
