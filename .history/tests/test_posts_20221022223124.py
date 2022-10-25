def test_get_every_post(authorized_client):
    authorized_client.get('/posts/')
