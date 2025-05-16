import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

from reviews.models import Reviews

pytestmark = pytest.mark.django_db


def test_list_reviews_unauthenticated(api_client, create_review, create_category, create_place, normal_user, create_user):
    cat = create_category(name='CatR', slug='catr')
    place = create_place(category=cat)
    create_review(place=place, user=normal_user, text='R1')
    create_review(place=place, user=create_user(
        email='other1@example.com'), text='R2')
    url = reverse('reviews:review-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    texts = {r['text'] for r in response.data}
    assert {'R1', 'R2'} <= texts


def test_retrieve_review(api_client, create_review, create_category, create_place, normal_user):
    cat = create_category(name='CatDetailR', slug='detailr')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user, text='DetailR')
    url = reverse('reviews:review-detail', args=[review.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == review.id
    assert response.data['text'] == 'DetailR'
    assert 'price' in response.data and 'service' in response.data and 'interior' in response.data
    assert 'comment_count' in response.data
    assert 'self_content_type' in response.data


def test_by_place_action(api_client, create_review, create_category, create_place, normal_user):
    cat = create_category(name='CatBy', slug='by')
    place1 = create_place(name='Place1', slug='p1', category=cat)
    place2 = create_place(name='Place2', slug='p2', category=cat)
    create_review(place=place1, user=normal_user, text='ForPlace1')
    create_review(place=place2, user=normal_user, text='ForPlace2')
    url = reverse('reviews:review-by-place', args=[place1.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['text'] == 'ForPlace1'


def test_create_review_unauthenticated(api_client, create_category, create_place):
    cat = create_category(name='CatNewR', slug='newr')
    place = create_place(category=cat)
    url = reverse('reviews:review-list')
    data = {'place_id': place.id, 'text': 'NewR',
            'price': 3, 'service': 4, 'interior': 5}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_review_authenticated(auth_api_client, normal_user, create_category, create_place):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatAuthR', slug='authr')
    place = create_place(category=cat)
    url = reverse('reviews:review-list')
    data = {'place_id': place.id, 'user_id': normal_user.id,
            'text': 'AuthR', 'price': 4, 'service': 3, 'interior': 2}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == 'AuthR'
    assert response.data['user_id'] == normal_user.id


def test_update_review_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_review):
    cat = create_category(name='CatUpdR', slug='updr')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user,
                           text='Orig', price=1, service=1, interior=1)
    url = reverse('reviews:review-detail', args=[review.id])
    # другой пользователь
    other = normal_user.__class__.objects.create_user(
        email='other2@example.com', password='pass')
    auth_api_client.force_authenticate(user=other)
    resp = auth_api_client.patch(url, {'text': 'Updated'})
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # владелец
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.patch(url, {'text': 'Updated', 'price': 2})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['text'] == 'Updated'
    assert resp.data['price'] == 2


def test_delete_review_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_review):
    cat = create_category(name='CatDelR', slug='delr')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    url = reverse('reviews:review-detail', args=[review.id])
    # владелец не может удалить
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # администратор может удалить
    auth_api_client.force_authenticate(user=staff_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
