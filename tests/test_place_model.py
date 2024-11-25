import pytest
from reviews.models import Places, Categories
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_valid_name():
    """Тест: поле name заполнено корректно."""
    place = Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=None)
    assert place.name == "Кафе"


@pytest.mark.django_db
def test_name_exceeds_max_length():
    """Тест: поле name с длиной более 100 символов вызывает ValidationError."""
    long_name = "Кафе" * 30  # Длина строки > 100 символов
    place = Places(name=long_name, address="ул. Ленина, 1", category_id=None)
    with pytest.raises(ValidationError):
        place.full_clean()


@pytest.mark.django_db
def test_name_empty():
    """Тест: поле name не заполнено вызывает ValidationError."""
    place = Places(name="", address="ул. Ленина, 1", category_id=None)
    with pytest.raises(ValidationError):
        place.full_clean()


@pytest.mark.django_db
def test_valid_address():
    """Тест: поле address заполнено корректно."""
    place = Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=None)
    assert place.address == "ул. Ленина, 1"


@pytest.mark.django_db
def test_address_exceeds_max_length():
    """Тест: поле address с длиной более 100 символов вызывает ValidationError."""
    long_address = "ул. Ленина, 1" * 10  # Длина строки > 100 символов
    place = Places(name="Кафе", address=long_address, category_id=None)
    with pytest.raises(ValidationError):
        place.full_clean()


@pytest.mark.django_db
def test_address_empty():
    """Тест: поле address не заполнено вызывает ValidationError."""
    place = Places(name="Кафе", address="", category_id=None)
    with pytest.raises(ValidationError):
        place.full_clean()


@pytest.mark.django_db
def test_valid_category():
    """Тест: поле category_id заполнено корректно."""
    category = Categories.objects.create(name="Ресторан")
    place = Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=category)
    assert place.category_id == category


@pytest.mark.django_db
def test_category_empty():
    """Тест: поле category_id не заполнено допускается (может быть None)."""
    place = Places(name="Кафе", address="ул. Ленина, 1", category_id=None)
    place.full_clean()
    assert place.category_id is None


@pytest.mark.django_db
def test_category_deleted():
    """Тест: поле category_id становится None после удаления связанной категории."""
    category = Categories.objects.create(name="Ресторан")
    place = Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=category)
    category.delete()
    place.refresh_from_db()
    assert place.category_id is None


@pytest.mark.django_db
def test_slug_autogenerated():
    """Тест: поле slug генерируется автоматически на основе name."""
    place = Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=None)
    assert place.slug == "kafe"


@pytest.mark.django_db
def test_slug_unique():
    """Тест: поле slug должно быть уникальным."""
    Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=None)
    with pytest.raises(IntegrityError):
        Places.objects.create(
            name="Кафе", address="ул. Пушкина, 2", category_id=None)


@pytest.mark.django_db
def test_str_method():
    """Тест: метод __str__ возвращает значение поля name."""
    place = Places.objects.create(
        name="Кафе", address="ул. Ленина, 1", category_id=None)
    assert str(place) == "Кафе"
