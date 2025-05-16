import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_list_places_unauthenticated(api_client, create_place, create_category):
    # Создание тестовых данных
    cat = create_category(name='Cat', slug='cat')
    place1 = create_place(name='PlaceOne', address='Addr1', category=cat)
    place2 = create_place(name='PlaceTwo', address='Addr2', category=cat)

    url = reverse('reviews:place-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    returned_names = {p['name'] for p in response.data}
    assert {'PlaceOne', 'PlaceTwo'} <= returned_names


def test_retrieve_place(api_client, create_place):
    place = create_place(name='My Place', slug='my-place')
    url = reverse('reviews:place-detail', args=[place.slug])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == place.id
    assert response.data['name'] == 'My Place'
    assert response.data['slug'] == 'my-place'
    # Проверка дополнительных полей сериализатора
    assert 'photos' in response.data
    assert 'review_count' in response.data
    assert 'category_name' in response.data


def test_filter_places_by_name(api_client, create_place, create_category):
    cat = create_category(name='FilterCat', slug='filter-cat')
    create_place(name='AlphaPlace', category=cat)
    create_place(name='BetaPlace', category=cat)
    url = reverse('reviews:place-list') + '?name=Alpha'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    names = [p['name'] for p in response.data]
    assert names == ['AlphaPlace']


def test_create_place_unauthenticated(api_client, create_category):
    cat = create_category()
    url = reverse('reviews:place-list')
    data = {'name': 'NewPlace', 'address': 'Addr',
            'category_id': cat.id, 'about': 'About'}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_place_non_staff(auth_api_client, normal_user, create_category):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category()
    url = reverse('reviews:place-list')
    data = {'name': 'NewPlace', 'address': 'Addr',
            'category_id': cat.id, 'about': 'About'}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_place_staff(auth_api_client, staff_user, create_category):
    auth_api_client.force_authenticate(user=staff_user)
    cat = create_category()
    url = reverse('reviews:place-list')
    data = {'name': 'StaffPlace', 'address': 'Addr',
            'category_id': cat.id, 'about': 'About'}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'StaffPlace'
    assert response.data['slug']  # авто-сгенерированный слаг


def test_update_place_permissions(auth_api_client, create_place, normal_user, staff_user):
    place = create_place(name='Orig', slug='orig')
    url = reverse('reviews:place-detail', args=[place.slug])
    # non-staff
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.patch(url, {'name': 'Updated'})
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # staff
    auth_api_client.force_authenticate(user=staff_user)
    resp = auth_api_client.patch(url, {'name': 'Updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['name'] == 'Updated'


def test_delete_place_permissions(auth_api_client, create_place, normal_user, staff_user):
    place = create_place()
    url = reverse('reviews:place-detail', args=[place.slug])
    # non-staff
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # staff
    auth_api_client.force_authenticate(user=staff_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
