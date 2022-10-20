from argparse import OPTIONAL
from multiprocessing import synchronize
from random import randint, randrange
from re import L
from traceback import print_tb
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import get_db, engine
from . import models
from sqlalchemy.orm import Session


# ___this is our schema/pydantic model___
# it defines the structure of a request & response
# this insures the user will type exactly whats needed


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
# _____________________________________________


class PostCreate(PostBase):
    title: str
    content: str
    published: bool = True
