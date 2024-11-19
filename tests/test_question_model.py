import pytest
from reviews.models import Questions, Places
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

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
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    assert question.place_id == place

@pytest.mark.django_db
def test_place_id_empty(user):
    """Тест: поле place_id не заполнено вызывает IntegrityError."""
    with pytest.raises(IntegrityError):
        Questions.objects.create(place_id=None, user_id=user, text="Как работают по выходным?")

@pytest.mark.django_db
def test_place_deletion_cascades_to_questions(user, place):
    """Тест: при удалении place удаляется и question."""
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    place.delete()
    assert Questions.objects.filter(id=question.id).count() == 0

@pytest.mark.django_db
def test_user_id_filled_correctly(user, place):
    """Тест: поле user_id заполнено корректно."""
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    assert question.user_id == user

@pytest.mark.django_db
def test_user_id_empty(place):
    """Тест: поле user_id не заполнено вызывает IntegrityError."""
    with pytest.raises(IntegrityError):
        Questions.objects.create(place_id=place, user_id=None, text="Как работают по выходным?")

@pytest.mark.django_db
def test_user_deletion_cascades_to_questions(user, place):
    """Тест: при удалении user удаляется и question."""
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    user.delete()
    assert Questions.objects.filter(id=question.id).count() == 0

@pytest.mark.django_db
def test_text_filled_correctly(user, place):
    """Тест: поле text заполнено корректно."""
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    assert question.text == "Как работают по выходным?"

@pytest.mark.django_db
def test_text_exceeds_max_length(user, place):
    """Тест: поле text превышает максимальную длину."""
    long_text = "x" * 201
    with pytest.raises(ValidationError):
        question = Questions(place_id=place, user_id=user, text=long_text)
        question.full_clean()

@pytest.mark.django_db
def test_text_empty(user, place):
    """Тест: поле text не заполнено вызывает ValidationError."""
    with pytest.raises(ValidationError):
        question = Questions(place_id=place, user_id=user, text="")
        question.full_clean()

@pytest.mark.django_db
def test_created_at_autofilled(user, place):
    """Тест: поле created_at заполняется автоматически."""
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    assert question.created_at is not None

@pytest.mark.django_db
def test_str_method(user, place):
    """Тест: метод __str__ возвращает корректное значение."""
    question = Questions.objects.create(place_id=place, user_id=user, text="Как работают по выходным?")
    expected_str = f"{question.user_id} {question.place_id} {question.text[:30]}"
    assert str(question) == expected_str
