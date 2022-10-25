from urllib import response
from app import schemas
from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_get_all_post(authorized_client):
    res = authorized_client.get('/posts/')
    print(res.json())
    assert res.status_code == 200
