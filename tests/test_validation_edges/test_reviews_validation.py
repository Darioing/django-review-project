import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_create_review_with_invalid_price(admin_api_client, place, normal_user):
    url = reverse('reviews:review-list')
    data = {
        'place_id': place.id,
        'user_id': normal_user.id,
        'price': 10,  # вне диапазона 1-5
        'service': 3,
        'interior': 3,
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'price' in response.data


@pytest.mark.django_db
def test_create_review_with_invalid_service(admin_api_client, place, normal_user):
    url = reverse('reviews:review-list')
    data = {
        'place_id': place.id,
        'user_id': normal_user.id,
        'price': 3,
        'service': 0,  # ниже допустимого минимума
        'interior': 3,
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'service' in response.data


@pytest.mark.django_db
def test_create_review_with_invalid_interior(admin_api_client, place, normal_user):
    url = reverse('reviews:review-list')
    data = {
        'place_id': place.id,
        'user_id': normal_user.id,
        'price': 3,
        'service': 3,
        'interior': 6,  # выше допустимого максимума
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'interior' in response.data


@pytest.mark.django_db
def test_create_duplicate_review(admin_api_client, place, normal_user, review, create_review):
    # review — уже созданный объект отзыва для данной пары user + place
    # теперь пытаемся создать дубликат
    url = reverse('reviews:review-list')
    data = {
        'place_id': place.id,
        'user_id': normal_user.id,
        'text': 'Duplicate review',
        'price': 4,
        'service': 4,
        'interior': 4
    }

    admin_api_client.force_authenticate(user=normal_user)
    response = admin_api_client.post(url, data)

    assert response.status_code == 400
    assert 'non_field_errors' in response.data
