# tests/conftest.py
import pytest
import django
from django.conf import settings
from django.urls import reverse, resolve


def pytest_configure():
    django.setup()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_user(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    def make_user(**kwargs):
        return User.objects.create_user(
            email=kwargs.get('email', 'test@example.com'),
            password=kwargs.get('password', 'testpass123'),
            FIO=kwargs.get('FIO', 'Test User')
        )
    return make_user
