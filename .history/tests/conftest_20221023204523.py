
from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# initializing our database parameters
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# engine is the lowest level object used by SQLAlchemy. It maintains a pool of connections available for use whenever the application needs to talk to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Session is an interface for SELECT and other queries
TestingSessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# pytest fixtures predefine what parameters and results to expect if a function is ran
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db  # as per FastaAPI docs
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {'email': '1qwpba9pp@gmail.com', 'password': 'qasdf'}
    response = client.post('/users/', json=user_data)

    assert response.status_code == 201
    print(response.json())
    newly_created_user = response.json()
    newly_created_user['password'] = user_data['password']
    return newly_created_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session):
    post_data = [{
        'title': 'first title',
        'content': 'first content',
        'owner_id': test_user['id']
    },
        {
        'title': '2nd title',
        'content': '2nd content',
        'owner_id': test_user['id']
    }, {
        'title': '3rd title',
        'content': '3rd content',
        'owner_id': test_user['id']
    }]
    session.add
