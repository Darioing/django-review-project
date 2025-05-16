import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_create_place_with_empty_name(admin_api_client, create_category):
    url = reverse('reviews:place-list')
    data = {
        'name': '',
        'address': 'Some address',
        'category_id': create_category().id
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_place_with_empty_address(admin_api_client, create_category):
    url = reverse('reviews:place-list')
    data = {
        'name': 'Some Place',
        'address': '',
        'category_id': create_category().id
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'address' in response.data


@pytest.mark.django_db
def test_create_place_with_null_category(admin_api_client):
    url = reverse('reviews:place-list')
    data = {
        'name': 'Test Place',
        'address': 'Some address',
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['category_id'] is None


@pytest.mark.django_db
def test_create_place_with_blank_category(admin_api_client):
    url = reverse('reviews:place-list')
    data = {
        'name': 'Test Place',
        'address': 'Some address'
        # category_id omitted
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['category_id'] is None
