from urllib import response
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    print('tseting root')
