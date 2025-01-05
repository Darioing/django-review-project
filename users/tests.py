import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(email, password, **kwargs):
        user = User.objects.create_user(
            email=email, password=password, **kwargs)
        return user
    return make_user


class TestUserRegistration:
    @pytest.mark.django_db
    def test_registration_success(self, api_client):
        response = api_client.post('/user/register/', {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'FIO': 'Test User'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['message'] == 'User registered successfully!'

    @pytest.mark.django_db
    def test_registration_missing_fields(self, api_client):
        response = api_client.post('/user/register/', {
            'email': '',
            'password': '',
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.json()
        assert 'password' in response.json()

    @pytest.mark.django_db
    def test_registration_duplicate_email(self, api_client, create_user):
        create_user(email='existing@example.com', password='password')
        response = api_client.post('/user/register/', {
            'email': 'existing@example.com',
            'password': 'testpassword123',
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.json()


class TestUserLogin:
    @pytest.mark.django_db
    def test_login_success(self, api_client, create_user):
        create_user(email='testuser@example.com',
                    password='testpassword123', is_active=True)
        response = api_client.post('/user/token/', {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        })
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.json()
        assert 'refresh' in response.json()

    @pytest.mark.django_db
    def test_login_invalid_credentials(self, api_client):
        response = api_client.post('/user/token/', {
            'email': 'fake@mail.com',
            'password': 'wrongpassword',
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'access' not in response.json()

    @pytest.mark.django_db
    def test_login_missing_fields(self, api_client):
        response = api_client.post('/user/token/', {
            'email': '',
            'password': '',
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.json()

    @pytest.mark.django_db
    def test_protected_view_authenticated(self, api_client, create_user):
        user = create_user(email='testuser@example.com',
                           password='testpassword123')
        response = api_client.post('/user/token/', {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        })
        access_token = response.json()['access']
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = api_client.get('/user/protected/')
        print(response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == 'Вы авторизованы!'

    @pytest.mark.django_db
    def test_protected_view_unauthenticated(self, api_client):
        response = api_client.get('/user/protected/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
