from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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


"""this is used if you want to connect to PostgreSQL without using SQLalchemy"""
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='APIdatabase',
#                                 user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break
#     except Exception as error:
#         print(f'conn failed, {error}')
#         time.sleep(2)
