import pytest
from rabble.tests.factories import *
from django.urls import reverse
from rabble.models import SubRabble, Post, Comment

@pytest.mark.django_db
def test_index_view(client):
    community = CommunityFactory.create()
    client.force_login(community.owner)

    subrabbles = SubRabbleFactory.create_batch(5, rabble_id=community)

    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

    assert 'rabbles' in response.context
    assert community in response.context['rabbles']

    html = response.content.decode()
    assert community.community_id in html
    assert str(community.members.count()) in html


@pytest.mark.django_db
def test_subrabble_detail_view(client):
    community = CommunityFactory.create()
    client.force_login(community.owner)

    subrabble = SubRabbleFactory.create(rabble_id=community)

    posts = []
    for _ in range(5):
        post = PostFactory.create(subrabble_id=subrabble, user_id=community.owner)
        posts.append(post)
        CommentFactory.create(post_id=post, user_id=community.owner)

    url = reverse('subrabble-detail', kwargs={
        'community_id': community.community_id,
        'subrabble_community_id': subrabble.subrabble_community_id
    })
    response = client.get(url)
    assert response.status_code == 200

    rendered_posts = list(response.context['posts'])
    assert set(rendered_posts) == set(posts)

    html = response.content.decode()
    for post in posts:
        assert post.title in html

        count = Comment.objects.filter(post_id=post).count()
        assert str(count) in html


@pytest.mark.django_db
def test_post_create_view(client):
    community = CommunityFactory.create()
    client.force_login(community.owner)

    subrabble = SubRabbleFactory.create(rabble_id=community)

    url = reverse('post-create', kwargs={
        'community_id': community.community_id,
        'subrabble_community_id': subrabble.subrabble_community_id
    })
    form_data = {
        'title': 'My New Post',
        'body': 'Hello, world!',
    }
    response = client.post(url, form_data)

    assert response.status_code == 302
    post = Post.objects.get(title='My New Post', subrabble_id=subrabble)
    assert post.body == 'Hello, world!'
    assert post.user_id == community.owner

    expected = reverse(
        'post-detail',
        kwargs={
            'community_id': community.community_id,
            'subrabble_community_id': subrabble.subrabble_community_id,
            'pk': post.pk
        }
    )
    assert response.url.endswith(expected)
