from app import schemas
from .testdatabase import client, session


def test_root(client):
    response = client.get('/')
    print(response.json().get("status"))
    assert response.json().get("status") == 'mainkek.py'
    assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        '/users/', json={'email': '1wpba9pp@gmail.com', 'password': 'asdf'})

    new_user = schemas.ShowUser(**response.json())
    assert new_user.email == '1wpba9pp@gmail.com'
    assert response.status_code == 201


def test_login(client):
    response = client.post(
        '/login', data={'email': '1wpba9pp@gmail.com', 'password': 'asdf'})

    new_user = schemas.ShowUser(**response.json())
    assert new_user.email == '1wpba9pp@gmail.com'
    assert response.status_code == 201
    # you can also perform the test this way, without schemas and pydantic
    # def test_create_user():
    #     response = client.post(
    #         '/users/', json={'email': 'pp9pp@gmail.com', 'password': 'asdf'})

    #     print(response.json())
    #     assert response.json().get('email') == 'pp9pp@gmail.com'
    #     assert response.status_code == 201
