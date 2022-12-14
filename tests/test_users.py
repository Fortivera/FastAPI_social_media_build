from app import schemas
from app import schemas
from jose import jwt
from app.config import settings
import pytest


# collection of tests that check trivial performance of the liking functionality


def test_root(client):
    response = client.get('/')
    print(response.json().get("status"))
    assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        '/users/', json={'email': '1wpba9pp@gmail.com', 'password': 'asdf'})

    new_user = schemas.ShowUser(**response.json())
    assert new_user.email == '1wpba9pp@gmail.com'
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})
    # testing the token validation
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get('user_id')

    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
    ('incorrect', 'qasdf', 403),
    ('1qwpba9pp@gmail.com', 'incorrect', 403),
    ('incorrect', 'incorrect', 403),
    (None, 'qasdf', 422),
    ('1qwpba9pp@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post(
        '/login', data={'username': email, 'password': password})

    assert response.status_code == status_code

    # you can also perform the test this way, without schemas and pydantic
    # def test_create_user():
    #     response = client.post(
    #         '/users/', json={'email': 'pp9pp@gmail.com', 'password': 'asdf'})

    #     print(response.json())
    #     assert response.json().get('email') == 'pp9pp@gmail.com'
    #     assert response.status_code == 201
