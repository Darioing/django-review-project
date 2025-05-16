# tests/test_auth.py
import pytest
import os
import json
from datetime import datetime, timedelta
from django.conf import settings
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

    # Проверяем промежуточный ответ
    assert response.status_code == status.HTTP_200_OK
    assert 'test_link' in response.data

    # Проверяем создание временного файла
    token = response.data['test_link'].split('/')[-2]
    pending_file = os.path.join(
        settings.BASE_DIR, 'pending_users', f"{token}.json")
    assert os.path.exists(pending_file)

    # Проверяем содержимое файла
    with open(pending_file) as f:
        user_data = json.load(f)
        assert user_data['email'] == 'test@example.com'
        assert user_data['FIO'] == 'Test User'


@pytest.mark.django_db
def test_user_registration_invalid_data(api_client):
    url = reverse('users:register')
    data = {
        'email': 'invalid-email',
        'FIO': '',
        'password': '123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data
    assert 'FIO' in response.data
    assert 'password' in response.data


@pytest.mark.django_db
def test_email_verification_success(api_client):
    # 1. Сначала регистрируем пользователя
    reg_url = reverse('users:register')
    reg_data = {
        'email': 'verify@example.com',
        'FIO': 'Verify User',
        'password': 'verifypass123'
    }
    reg_response = api_client.post(reg_url, reg_data, format='json')
    token = reg_response.data['test_link'].split('/')[-2]

    # 2. Вызываем эндпоинт подтверждения
    verify_url = reverse('users:verify-email', kwargs={'token': token})
    response = api_client.get(verify_url)

    # Проверяем редирект
    assert response.status_code == status.HTTP_302_FOUND
    assert settings.FRONTEND_URL in response.url

    # Проверяем, что пользователь создан в БД
    from django.contrib.auth import get_user_model
    User = get_user_model()
    assert User.objects.filter(email='verify@example.com').exists()

    # Проверяем удаление временного файла
    pending_file = os.path.join(
        settings.BASE_DIR, 'pending_users', f"{token}.json")
    assert not os.path.exists(pending_file)


@pytest.mark.django_db
def test_email_verification_invalid_token(api_client):
    # Пытаемся подтвердить несуществующий токен
    verify_url = reverse('users:verify-email',
                         kwargs={'token': 'invalid-token'})
    response = api_client.get(verify_url)

    assert response.status_code == status.HTTP_302_FOUND
    assert 'login' in response.url
    assert 'error=invalid_token' in response.url


@pytest.mark.django_db
def test_email_verification_expired_token(api_client):
    # 1. Создаем "просроченный" файл вручную
    pending_dir = os.path.join(settings.BASE_DIR, 'pending_users')
    os.makedirs(pending_dir, exist_ok=True)

    expired_token = 'expired-token-123'
    expired_file = os.path.join(pending_dir, f"{expired_token}.json")

    expired_data = {
        'email': 'expired@example.com',
        'FIO': 'Expired User',
        'password': 'expiredpass123',
        'token': expired_token,
        'created_at': (datetime.now() - timedelta(days=2)).isoformat()
    }

    with open(expired_file, 'w') as f:
        json.dump(expired_data, f)

    # 2. Пытаемся подтвердить
    verify_url = reverse('users:verify-email', kwargs={'token': expired_token})
    response = api_client.get(verify_url)

    assert response.status_code == status.HTTP_302_FOUND
    assert 'login' in response.url
    assert 'error=expired_token' in response.url


@pytest.mark.django_db
def test_email_file_creation(api_client):
    url = reverse('users:register')
    test_email = 'filetest@example.com'
    data = {
        'email': test_email,
        'FIO': 'File Test',
        'password': 'filetest123'
    }
    response = api_client.post(url, data, format='json')

    # Проверяем создание файла с ссылкой
    email_file = os.path.join(
        settings.BASE_DIR, 'email_links', f"{test_email}.txt")
    assert os.path.exists(email_file)

    # Проверяем содержимое файла
    with open(email_file) as f:
        content = f.read()
        assert 'Ссылка для подтверждения' in content


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
    url = reverse('users:custom_login')
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
    url = reverse('users:custom_login')
    data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'  # Неверный пароль
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_protected_view_without_token(api_client):
    url = reverse('users:protected')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_protected_view_with_token(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    login_url = reverse('users:custom_login')
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    token_response = api_client.post(login_url, login_data, format='json')
    access_token = token_response.data['access']

    # Тестируем защищённый эндпоинт с токеном
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    protected_url = reverse('users:protected')
    response = api_client.get(protected_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Вы авторизованы!'


@pytest.mark.django_db
def test_user_profile_me(api_client, create_user):
    user = create_user(email='test@example.com', password='testpass123')
    login_url = reverse('users:custom_login')
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    token_response = api_client.post(login_url, login_data, format='json')
    access_token = token_response.data['access']

    # Получаем профиль
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    profile_url = reverse('users:profile-me')
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
    # 1. Создаем пользователя
    user = create_user(email='test@example.com', password='testpass123')

    # 2. Логинимся (получаем токены)
    login_url = reverse('users:custom_login')
    login_response = api_client.post(login_url, {
        'email': 'test@example.com',
        'password': 'testpass123'
    }, format='json')

    assert login_response.status_code == status.HTTP_200_OK
    refresh_token = login_response.data['refresh']
    access_token = login_response.data['access']

    # 3. Выходим (передаем refresh token)
    logout_url = reverse('users:logout')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    logout_response = api_client.post(
        logout_url,
        {'refresh': refresh_token},
        format='json'
    )

    # Проверяем успешный ответ от logout
    assert logout_response.status_code == status.HTTP_200_OK
    assert logout_response.data['message'] == 'Вы успешно вышли из аккаунта.'

    # 4. Проверяем, что refresh token больше не работает
    refresh_url = reverse('users:token_refresh')
    refresh_response = api_client.post(
        refresh_url,
        {'refresh': refresh_token},
        format='json'
    )
    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture(autouse=True)
def cleanup_files():
    """Очищает тестовые файлы после каждого теста"""
    yield
    import shutil
    pending_dir = os.path.join(settings.BASE_DIR, 'pending_users')
    email_dir = os.path.join(settings.BASE_DIR, 'email_links')

    if os.path.exists(pending_dir):
        shutil.rmtree(pending_dir)
    if os.path.exists(email_dir):
        shutil.rmtree(email_dir)
