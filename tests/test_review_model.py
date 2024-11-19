import pytest
from reviews.models import Reviews, Places
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

User = get_user_model()

@pytest.fixture
def user():
    """Фикстура для создания объекта User."""
    return User.objects.create(first_name="test", second_name="user", email="test@user.ru", password="password")

@pytest.fixture
def place():
    """Фикстура для создания объекта Places."""
    return Places.objects.create(name="Кафе", address="ул. Ленина, 1", category_id=None)

@pytest.mark.django_db
def test_place_id_filled_correctly(user, place):
    """Тест: поле place_id заполнено корректно."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.place_id == place

@pytest.mark.django_db
def test_place_id_empty(user):
    """Тест: поле place_id не заполнено вызывает IntegrityError."""
    with pytest.raises(IntegrityError):
        Reviews.objects.create(place_id=None, user_id=user, text="Отличное место", price=5, service=4, interior=3)

@pytest.mark.django_db
def test_place_deletion_cascades_to_reviews(user, place):
    """Тест: при удалении place удаляется и review."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    place.delete()
    assert Reviews.objects.all().count() == 0

@pytest.mark.django_db
def test_user_id_filled_correctly(user, place):
    """Тест: поле user_id заполнено корректно."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.user_id == user

@pytest.mark.django_db
def test_user_id_empty(place):
    """Тест: поле user_id не заполнено вызывает IntegrityError."""
    with pytest.raises(IntegrityError):
        Reviews.objects.create(place_id=place, user_id=None, text="Отличное место", price=5, service=4, interior=3)

@pytest.mark.django_db
def test_user_deletion_cascades_to_reviews(user, place):
    """Тест: при удалении user удаляется и review."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    user.delete()
    assert Reviews.objects.all().count() == 0

@pytest.mark.django_db
def test_text_filled_correctly(user, place):
    """Тест: поле text заполнено корректно."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.text == "Отличное место"

@pytest.mark.django_db
def test_text_exceeds_max_length(user, place):
    """Тест: поле text превышает максимальную длину."""
    long_text = "x" * 501
    with pytest.raises(ValidationError):
        review = Reviews.objects.create(place_id=place, user_id=user, text=long_text, price=5, service=4, interior=3)
        review.full_clean()

@pytest.mark.django_db
def test_text_empty(user, place):
    """Тест: поле text не заполнено."""
    review = Reviews.objects.create(place_id=place, user_id=user, text=None, price=5, service=4, interior=3)
    assert review.text is None

@pytest.mark.django_db
def test_price_filled_correctly(user, place):
    """Тест: поле price заполнено корректно."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.price == 5

@pytest.mark.django_db
def test_price_below_min(user, place):
    """Тест: поле price меньше минимального значения вызывает ValidationError."""
    with pytest.raises(ValidationError):
        review = Reviews(place_id=place, user_id=user, text="Отличное место", price=0, service=4, interior=3)
        review.full_clean()

@pytest.mark.django_db
def test_price_above_max(user, place):
    """Тест: поле price больше максимального значения вызывает ValidationError."""
    with pytest.raises(ValidationError):
        review = Reviews(place_id=place, user_id=user, text="Отличное место", price=6, service=4, interior=3)
        review.full_clean()

@pytest.mark.django_db
def test_service_filled_correctly(user, place):
    """Тест: поле service заполнено корректно."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.service == 4

@pytest.mark.django_db
def test_service_below_min(user, place):
    """Тест: поле service меньше минимального значения вызывает ValidationError."""
    with pytest.raises(ValidationError):
        review = Reviews(place_id=place, user_id=user, text="Отличное место", price=5, service=0, interior=3)
        review.full_clean()

@pytest.mark.django_db
def test_service_above_max(user, place):
    """Тест: поле service больше максимального значения вызывает ValidationError."""
    with pytest.raises(ValidationError):
        review = Reviews(place_id=place, user_id=user, text="Отличное место", price=5, service=6, interior=3)
        review.full_clean()

@pytest.mark.django_db
def test_interior_filled_correctly(user, place):
    """Тест: поле interior заполнено корректно."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.interior == 3

@pytest.mark.django_db
def test_interior_below_min(user, place):
    """Тест: поле interior меньше минимального значения вызывает ValidationError."""
    with pytest.raises(ValidationError):
        review = Reviews(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=0)
        review.full_clean()

@pytest.mark.django_db
def test_interior_above_max(user, place):
    """Тест: поле interior больше максимального значения вызывает ValidationError."""
    with pytest.raises(ValidationError):
        review = Reviews(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=6)
        review.full_clean()

@pytest.mark.django_db
def test_created_at_autofilled(user, place):
    """Тест: поле created_at заполняется автоматически."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    assert review.created_at is not None

@pytest.mark.django_db
def test_str_method(user, place):
    """Тест: метод __str__ возвращает корректное значение."""
    review = Reviews.objects.create(place_id=place, user_id=user, text="Отличное место", price=5, service=4, interior=3)
    expected_str = f"{review.user_id} {review.place_id} {review.text[:30]}"
    assert str(review) == expected_str
