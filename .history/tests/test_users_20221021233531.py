from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

client = TestClient(app)


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def override_get_db():
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()


def test_root():
    response = client.get('/')
    print(response.json().get("status"))
    assert response.json().get("status") == 'mainkek.py'
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        '/users/', json={'email': 'pp9pp@gmail.com', 'password': 'asdf'})

    new_user = schemas.ShowUser(**response.json())
    assert new_user.email == 'pp9pp@gmail.com'
    assert response.status_code == 201

# you can also perform the test this way, without schemas and pydantic
# def test_create_user():
#     response = client.post(
#         '/users/', json={'email': 'pp9pp@gmail.com', 'password': 'asdf'})

#     print(response.json())
#     assert response.json().get('email') == 'pp9pp@gmail.com'
#     assert response.status_code == 201
