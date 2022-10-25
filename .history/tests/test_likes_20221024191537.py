
def test_post_like(authorized_client, test_posts):
    liked = authorized_client.post('/like/', json={})
