import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
def test_create_category_with_empty_name(admin_api_client):
    url = reverse('reviews:category-list')
    data = {'name': ''}
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_category_with_null_name(admin_api_client):
    url = reverse('reviews:category-list')
    data = {}  # не передаём name вообще
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data


@pytest.mark.django_db
def test_create_category_with_duplicate_name(admin_api_client, create_category):
    existing_category = create_category(name='Cafe')
    url = reverse('reviews:category-list')
    data = {'name': existing_category.name}
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
