from fastapi.testclient import TestClient
from app.main import app
from app import schemas
client = TestClient(app)


def test_root():
    response = client.get('/')
    print(response.json().get("status"))
    assert response.json().get("status") == 'mainkek.py'
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        '/users/', json={'email': 'pp10pp@gmail.com', 'password': 'asdf'})

    new_user = schemas.ShowUser(**response.json())
    assert new_user.email == 'pp10pp@gmail.com'
    assert response.status_code == 201
