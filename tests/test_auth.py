# tests/test_auth.py
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_registration_success(api_client):
    url = reverse('users:register')
    data = {
        'email': 'test@example.com',
        'FIO': 'Test User',
        'password': 'testpass123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User registered successfully!'


@pytest.mark.django_db
def test_user_registration_fail(api_client):
    url = reverse('users:register')
    data = {
        'email': 'invalid-email',  # Невалидный email
        'FIO': 'Test User',
        'password': 'testpass123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data


@pytest.mark.django_db
def test_jwt_login_success(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    url = reverse('users:login')
    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert 'user_id' in response.data  # Проверяем кастомное поле


@pytest.mark.django_db
def test_jwt_login_fail(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    url = reverse('users:login')
    data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'  # Неверный пароль
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_protected_view_without_token(api_client):
    url = reverse('protected')  # Замените на ваш URL
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_protected_view_with_token(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    login_url = reverse('users:login')
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    token_response = api_client.post(login_url, login_data, format='json')
    access_token = token_response.data['access']

    # Тестируем защищённый эндпоинт с токеном
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    protected_url = reverse('protected')  # Замените на ваш URL
    response = api_client.get(protected_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Вы авторизованы!'


@pytest.mark.django_db
def test_user_profile_me(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    login_url = reverse('users:login')
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    token_response = api_client.post(login_url, login_data, format='json')
    access_token = token_response.data['access']

    # Получаем профиль
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    # Проверьте имя URL в вашем urls.py
    profile_url = reverse('userprofile-me')
    response = api_client.get(profile_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == 'test@example.com'

    # Обновляем профиль
    update_data = {'FIO': 'Updated Name'}
    response = api_client.patch(profile_url, update_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['FIO'] == 'Updated Name'


@pytest.mark.django_db
def test_logout(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    login_url = reverse('users:login')
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    token_response = api_client.post(login_url, login_data, format='json')
    refresh_token = token_response.data['refresh']

    # Выход из системы
    logout_url = reverse('users:logout')
    response = api_client.post(
        logout_url, {'refresh': refresh_token}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Вы успешно вышли из аккаунта.'

    # Проверяем, что токен больше не работает
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token_response.data["access"]}')
    protected_url = reverse('protected-view')  # Замените на ваш URL
    response = api_client.get(protected_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
