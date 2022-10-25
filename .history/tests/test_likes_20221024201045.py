from urllib import response
import pytest
from app import models


@pytest.fixture()
def test_like(test_posts, session, test_user):
    new_like = models.Like(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_post_like(authorized_client, test_posts):
    response = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "like_status": 1})  # using the schemas format for likes
    assert response.status_code == 201


def test_like_twice_post(authorized_client, test_posts, test_like):
    response = authorized_client.post(
        '/like/', json={"post_id": test_posts[3].id, "like_status": 1})
    assert response.status_code == 409


def test_delete_like_successfull(authorized_client, test_posts):
    response = authorized_client.post("/like/", test_posts[3].id, "like_status": 0)
    assert response.status_code == 201
