import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

pytestmark = pytest.mark.django_db

# test invalid vote_type accepted by API


def test_create_vote_with_invalid_type(admin_api_client, create_comment, create_user):
    user = create_user(email='user2@example.com')
    comment = create_comment(user=user, text='EdgeComment2')
    ct = ContentType.objects.get_for_model(comment)
    url = reverse('reviews:vote-list')
    data = {'user_id': user.id, 'content_type': ct.id,
            'object_id': comment.id, 'vote_type': 0}
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'total_votes' in response.data

# invalid content_type


@pytest.mark.django_db
def test_create_vote_with_invalid_content_type(admin_api_client, create_comment, create_user):
    user = create_user(email='user3@example.com')
    comment = create_comment(user=user, text='EdgeComment3')
    url = reverse('reviews:vote-list')
    data = {'user_id': user.id, 'content_type': 999999,
            'object_id': comment.id, 'vote_type': 1}
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'content_type' in response.data

# update existing vote


@pytest.mark.django_db
def test_update_existing_vote_changes_total(admin_api_client, create_comment, create_user):
    user = create_user(email='user4@example.com')
    comment = create_comment(user=user, text='EdgeComment4')
    ct = ContentType.objects.get_for_model(comment)
    url = reverse('reviews:vote-list')
    data = {'user_id': user.id, 'content_type': ct.id,
            'object_id': comment.id, 'vote_type': 1}
    resp1 = admin_api_client.post(url, data)
    assert resp1.status_code == status.HTTP_200_OK
    assert resp1.data['total_votes'] == 1
    data['vote_type'] = -1
    resp2 = admin_api_client.post(url, data)
    assert resp2.status_code == status.HTTP_200_OK
    assert resp2.data['total_votes'] == -1

# duplicate vote returns update


@pytest.mark.django_db
def test_create_duplicate_vote_same_user_returns_update(admin_api_client, create_comment, create_user):
    user = create_user(email='user5@example.com')
    comment = create_comment(user=user, text='EdgeComment5')
    ct = ContentType.objects.get_for_model(comment)
    url = reverse('reviews:vote-list')
    data = {'user_id': user.id, 'content_type': ct.id,
            'object_id': comment.id, 'vote_type': 1}
    resp1 = admin_api_client.post(url, data)
    resp2 = admin_api_client.post(url, data)
    assert resp2.status_code == status.HTTP_200_OK
    assert resp2.data['total_votes'] == 1
