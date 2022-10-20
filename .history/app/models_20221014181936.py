from email import contentmanager
from turtle import title
import sqlalchemy


from sqlalchemy import TIME, Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = 'posts'

    id
    title
    content
    published
    created_at = Column(TIMESTAMP(timezone=True))
