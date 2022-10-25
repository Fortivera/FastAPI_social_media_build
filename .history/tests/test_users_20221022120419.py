from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import schemas
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)


def test_root(client):
    response = client.get('/')
    print(response.json().get("status"))
    assert response.json().get("status") == 'mainkek.py'
    assert response.status_code == 200


def test_create_user(client):
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
