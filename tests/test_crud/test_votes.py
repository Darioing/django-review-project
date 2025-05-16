import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

pytestmark = pytest.mark.django_db


def test_list_votes_unauthenticated(api_client, create_vote, create_category, create_place, create_review, normal_user, create_user):
    cat = create_category(name='CatV', slug='catv')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    create_vote(review=review, user=normal_user, vote_type=1)
    create_vote(review=review, user=create_user(
        email='otherv@example.com'), vote_type=-1)
    url = reverse('reviews:vote-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    types = {v['vote_type'] for v in response.data}
    assert {1, -1} <= types


def test_create_vote_unauthenticated(api_client, create_category, create_place, create_review):
    cat = create_category(name='CatNewV', slug='newv')
    place = create_place(category=cat)
    review = create_review(place=place)
    ct = ContentType.objects.get_for_model(review)
    url = reverse('reviews:vote-list')
    data = {'content_type': ct.id, 'object_id': review.id, 'vote_type': 1}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_vote_authenticated(auth_api_client, normal_user, create_category, create_place, create_review):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatAuthV', slug='authv')
    place = create_place(category=cat)
    review = create_review(place=place)
    ct = ContentType.objects.get_for_model(review)
    url = reverse('reviews:vote-list')
    data = {'content_type': ct.id, 'object_id': review.id, 'vote_type': 1}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == 'Vote processed successfully'
    assert 'total_votes' in response.data


def test_update_vote(auth_api_client, normal_user, create_category, create_place, create_review, create_vote):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatUpdV', slug='updv')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    vote = create_vote(review=review, user=normal_user, vote_type=1)
    url = reverse('reviews:vote-detail', args=[vote.id])
    response = auth_api_client.patch(url, {'vote_type': -1})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['vote_type'] == -1


def test_delete_vote_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_review, create_vote):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatDelV', slug='delv')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    vote = create_vote(review=review, user=normal_user)
    url = reverse('reviews:vote-detail', args=[vote.id])
    response = auth_api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_total_votes_action(api_client, create_category, create_place, create_review, create_vote, create_user):
    cat = create_category(name='CatTotalV', slug='totalv')
    place = create_place(category=cat)
    review = create_review(place=place)
    ct = ContentType.objects.get_for_model(review)
    create_vote(review=review, user=create_user(
        email='u1@example.com'), vote_type=1)
    create_vote(review=review, user=create_user(
        email='u2@example.com'), vote_type=1)
    url = reverse('reviews:vote-total-votes') + \
        f'?content_type={ct.id}&object_id={review.id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['total_votes'] == 2


def test_user_vote_action(auth_api_client, normal_user, create_category, create_place, create_review, create_vote):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatUserV', slug='userv')
    place = create_place(category=cat)
    review = create_review(place=place)
    ct = ContentType.objects.get_for_model(review)
    create_vote(review=review, user=normal_user, vote_type=1)
    url = reverse('reviews:vote-user-vote') + \
        f'?content_type={ct.id}&object_id={review.id}'
    response = auth_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['user_vote'] == 1
