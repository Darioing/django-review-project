import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user_success():
    """Тест успешного создания пользователя."""
    user = User.objects.create_user(
        email="testuser@example.com",
        password="securepassword",
        first_name="Test",
        second_name="User"
    )
    assert user.email == "testuser@example.com"
    assert user.check_password("securepassword") is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_superuser_success():
    """Тест успешного создания суперпользователя."""
    superuser = User.objects.create_superuser(
        email="admin@example.com",
        password="securepassword",
        first_name="Admin",
        second_name="User"
    )
    assert superuser.email == "admin@example.com"
    assert superuser.is_staff is True
    assert superuser.is_superuser is True


@pytest.mark.django_db
def test_create_user_without_email():
    """Тест создания пользователя без email (ожидаем ошибку)."""
    with pytest.raises(ValueError, match="The given email must be set"):
        User.objects.create_user(
            email=None,
            password="securepassword",
            first_name="Test",
            second_name="User"
        )


@pytest.mark.django_db
def test_create_user_without_required_fields():
    """Тест создания пользователя без обязательных полей."""
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email="testuser@example.com",
            password="securepassword",
            first_name=None,
            second_name=None
        )


@pytest.mark.django_db
def test_superuser_invalid_fields():
    """Тест создания суперпользователя с некорректными флагами."""
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser(
            email="superuser@example.com",
            password="securepassword",
            first_name="Super",
            second_name="User",
            is_staff=False
        )

    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        User.objects.create_superuser(
            email="superuser@example.com",
            password="securepassword",
            first_name="Super",
            second_name="User",
            is_superuser=False
        )

@pytest.mark.django_db
def test_max_length_first_name():
    """Тест на проверку максимальной длины поля first_name."""
    long_name = "a" * 51  # Превышение на 1 символ
    user = User(
        email="testuser@example.com",
        password="securepassword",
        first_name=long_name,
        second_name="User"
    )
    with pytest.raises(ValidationError):  # Ловим исключение, если длина превышена
        user.full_clean()  # Вызывает валидацию


@pytest.mark.django_db
def test_max_length_second_name():
    """Тест на проверку максимальной длины поля second_name."""
    long_name = "a" * 51  # Превышение на 1 символ
    user = User(
        email="testuser@example.com",
        password="securepassword",
        first_name="User",
        second_name=long_name
    )
    with pytest.raises(ValidationError):  # Ловим исключение, если длина превышена
        user.full_clean()  # Вызывает валидацию


@pytest.mark.django_db
def test_max_length_email():
    """Тест на проверку максимальной длины email."""
    long_email = "a" * 245 + "@example.com"  # Максимальная длина email - 254
    user = User(
        email=long_email,
        password="securepassword",
        first_name="User",
        second_name="Name"
    )
    with pytest.raises(ValidationError):  # Ловим исключение, если длина превышена
        user.full_clean()  # Вызывает валидацию


@pytest.mark.django_db
def test_valid_password():
    """Тест на проверку корректного пароля."""
    user = User.objects.create_user(
        email="testuser@example.com",
        password="ComplexP@ssword123",
        first_name="Test",
        second_name="User"
    )
    assert user.check_password("ComplexP@ssword123") is True
