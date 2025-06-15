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
def test_post_detail_view(client):
    user = UserFactory.create()
    community = CommunityFactory.create(owner=user)
    subrabble = SubRabbleFactory.create(rabble_id=community, user_id=user)
    post = PostFactory.create(subrabble_id=subrabble, user_id=user)
    comment1 = CommentFactory.create(post_id=post, user_id=user, text="First comment")
    comment2 = CommentFactory.create(post_id=post, user_id=user, text="Second comment")

    client.force_login(user)

    url = reverse('post-detail', kwargs={
        'community_id': community.community_id,
        'subrabble_community_id': subrabble.subrabble_community_id,
        'pk': post.pk
    })

    response = client.get(url)
    assert response.status_code == 200
    assert 'post' in response.context
    assert response.context['post'] == post
    assert 'comments' in response.context
    assert list(response.context['comments'].order_by('id')) == [comment1, comment2]
    assert 'rabble' in response.context
    assert response.context['rabble'] == community
    assert 'subrabble' in response.context
    assert response.context['subrabble'] == subrabble


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
