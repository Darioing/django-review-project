import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_list_categories_unauthenticated(api_client):
    url = reverse('reviews:category-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


def test_retrieve_category(api_client, create_category):
    category = create_category(name='Cat1', slug='cat1')
    url = reverse('reviews:category-detail', args=[category.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == category.id
    assert response.data['name'] == 'Cat1'
    assert response.data['slug'] == 'cat1'


def test_create_category_unauthenticated(api_client):
    url = reverse('reviews:category-list')
    data = {'name': 'NewCat'}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_category_non_staff(auth_api_client, normal_user):
    auth_api_client.force_authenticate(user=normal_user)
    url = reverse('reviews:category-list')
    data = {'name': 'NewCat'}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_category_staff(auth_api_client, staff_user):
    auth_api_client.force_authenticate(user=staff_user)
    url = reverse('reviews:category-list')
    data = {'name': 'StaffCat'}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'StaffCat'
    assert 'slug' in response.data


def test_update_category_permissions(auth_api_client, create_category, normal_user, staff_user):
    category = create_category(name='Orig', slug='orig')
    # non-staff cannot update
    auth_api_client.force_authenticate(user=normal_user)
    url = reverse('reviews:category-detail', args=[category.id])
    response = auth_api_client.patch(url, {'name': 'Updated'})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # staff can update
    auth_api_client.force_authenticate(user=staff_user)
    response = auth_api_client.patch(url, {'name': 'Updated'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Updated'


def test_delete_category_permissions(auth_api_client, create_category, normal_user, staff_user):
    category = create_category()
    url = reverse('reviews:category-detail', args=[category.id])
    # non-staff cannot delete
    auth_api_client.force_authenticate(user=normal_user)
    response = auth_api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # staff can delete
    auth_api_client.force_authenticate(user=staff_user)
    response = auth_api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
