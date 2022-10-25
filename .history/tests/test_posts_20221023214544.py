from app import schemas


def test_get_every_post(test_posts, authorized_client):
    response = authorized_client.get('/posts/')

    def validating(post):
        return schemas.PostBack(**post)

    posts_map = map(validating, response.json())
    posts = list(posts_map)
    print(response.json())

    assert len(test_posts) == len(response.json())
    assert response.status_code == 200


def test_unauthorized_user_in_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_user_in_one_post(client, test_posts):
    response = client.get('/posts/{test_posts[]}')
    assert response.status_code == 401
