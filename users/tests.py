# # tests/conftest.py
# import pytest
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient

# User = get_user_model()


# @pytest.fixture
# def api_client():
#     return APIClient()


# @pytest.fixture
# def create_user():
#     def _create_user(**kwargs):
#         return User.objects.create_user(
#             email=kwargs.get('email', 'test@example.com'),
#             password=kwargs.get('password', 'testpass123'),
#             FIO=kwargs.get('FIO', 'Test User')
#         )
#     return _create_user
