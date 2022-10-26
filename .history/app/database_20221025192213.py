from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


#creation of the sql session and database
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

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
