import pytest
from django.core.exceptions import ValidationError
from reviews.models import Categories


@pytest.mark.django_db
def test_valid_name():
    """Тест: поле name заполнено корректно."""
    category = Categories.objects.create(name="Ресторан")
    assert category.name == "Ресторан"


@pytest.mark.django_db
def test_name_exceeds_max_length():
    """Тест: поле name с длиной более 50 символов вызывает ValidationError."""
    long_name = "Ресторан" * 10  # Длина строки > 50 символов
    category = Categories(name=long_name)
    with pytest.raises(ValidationError):
        category.full_clean()  # Вызывает валидацию модели


@pytest.mark.django_db
def test_name_empty():
    """Тест: поле name не заполнено."""
    category = Categories(name="")
    with pytest.raises(ValidationError):
        category.full_clean()  # Вызывает валидацию модели


@pytest.mark.django_db
def test_slug_autogenerated():
    """Тест: поле slug создается автоматически из поля name."""
    category = Categories.objects.create(name="Ресторан")
    assert category.slug == "restoran"  # Проверяем корректную транслитерацию


@pytest.mark.django_db
def test_str_method():
    """Тест: метод __str__ возвращает значение поля name."""
    category = Categories.objects.create(name="Ресторан")
    assert str(category) == "Ресторан"
