from turtle import title
from urllib import response
from app import schemas
import pytest


def test_get_every_post(test_posts, authorized_client):
    response = authorized_client.get('/posts/')

    def validating(post):
        return schemas.PostBack(**post)

    posts_map = map(validating, response.json())
    posts = list(posts_map)

    assert len(test_posts) == len(response.json())
    assert response.status_code == 200


def test_unauthorized_user_in_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_user_in_one_post(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_get_nonexisting_post(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/{00000}')
    assert response.status_code == 404


def test_get_valid_post(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostBack(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize('title, content, published', [
    ('title1', 'content1', True),
    ('title2', 'content2', True),
    ('title3', 'content3', False)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post(
        '/posts/', json={'title': title, 'content': content, 'published': published})

    post = schemas.Post(**response.json())
    print(test_user)
    assert post.id == test_user['id']
