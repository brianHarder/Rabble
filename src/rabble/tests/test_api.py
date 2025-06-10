import pytest
from rabble.tests.factories import *
from rest_framework.test import APIClient
from django.urls import reverse
from rabble.models import Post

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_subrabble_get(api_client):
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(rabble_id=community)

    response = api_client.get(reverse('api-subrabble', args=[
        community.community_id,
        subrabble.subrabble_community_id
    ]))
    assert response.status_code == 200

    data = response.json()
    assert data['subrabble_community_id'] == subrabble.subrabble_community_id
    assert data['subrabble_name'] == subrabble.subrabble_name
    assert data['description'] == subrabble.description
    assert data['allow_anonymous'] == subrabble.allow_anonymous
    assert data['private'] == subrabble.private
    assert data['rabble_id'] == community.pk


@pytest.mark.django_db
def test_post_patch(api_client):
    community = CommunityFactory.create()
    subrabble = SubRabbleFactory.create(rabble_id=community)
    post = PostFactory.create(subrabble_id=subrabble, user_id=community.owner)
    data = {'title': 'New Title'}

    response = api_client.patch(
        reverse('api-post-editor', args=[
            community.community_id,
            subrabble.subrabble_community_id,
            post.pk
        ]),
        data
    )
    assert response.status_code == 200

    post.refresh_from_db()
    assert post.title == data['title']
