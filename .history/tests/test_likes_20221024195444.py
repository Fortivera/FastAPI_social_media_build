import pytest


@pytest.fixture()
def test_like(test_posts, session, test_user):


def test_post_like(authorized_client, test_posts):
    response = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "like_status": 1})  # using the schemas format for likes
    assert response.status_code == 201


def test_like_twice_post(authorized_client, test_posts):
