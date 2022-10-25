from email import message
from urllib import response
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    print(response.json().get("status"))
    assert response.json().get("status") == mainlel.py
