import pytest
from reviews.models import Comments, Reviews, Questions, Places
from django.contrib.contenttypes.models import ContentType
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

@pytest.fixture
def review(user, place):
    """Фикстура для создания объекта Reviews."""
    return Reviews.objects.create(place_id=place, user_id=user, text="Отличное место!", price=5, service=5, interior=5)

@pytest.fixture
def question(user, place):
    """Фикстура для создания объекта Questions."""
    return Questions.objects.create(place_id=place, user_id=user, text="Когда открываетесь?")

@pytest.mark.django_db
def test_user_id_filled_correctly(user, review):
    """Тест: поле user_id заполнено корректно."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    assert comment.user_id == user

@pytest.mark.django_db
def test_user_id_empty(review):
    """Тест: поле user_id не заполнено вызывает IntegrityError."""
    content_type = ContentType.objects.get_for_model(Reviews)
    with pytest.raises(IntegrityError):
        Comments.objects.create(user_id=None, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")

@pytest.mark.django_db
def test_user_deletion_cascades_to_comments(user, review):
    """Тест: при удалении user удаляется и comment."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    user.delete()
    assert Comments.objects.filter(id=comment.id).count() == 0

@pytest.mark.django_db
def test_content_type_reviews_filled_correctly(user, review):
    """Тест: поле content_type заполняется типом объекта reviews."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    assert comment.content_type == content_type

@pytest.mark.django_db
def test_object_id_filled_correctly(user, review):
    """Тест: поле object_id заполнено корректно существующим объектом."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    assert comment.object_id == review.id

@pytest.mark.django_db
def test_content_object_filled_correctly(user, review):
    """Тест: поле content_object заполняется корректно."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    assert comment.content_object == review

@pytest.mark.django_db
def test_content_type_questions_filled_correctly(user, question):
    """Тест: поле content_type заполняется типом объекта questions."""
    content_type = ContentType.objects.get_for_model(Questions)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=question.id, text="Спасибо за информацию!")
    assert comment.content_type == content_type

@pytest.mark.django_db
def test_object_id_filled_correctly_questions(user, question):
    """Тест: поле object_id заполнено корректно существующим объектом."""
    content_type = ContentType.objects.get_for_model(Questions)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=question.id, text="Спасибо за информацию!")
    assert comment.object_id == question.id

@pytest.mark.django_db
def test_content_object_filled_correctly_questions(user, question):
    """Тест: поле content_object заполняется корректно."""
    content_type = ContentType.objects.get_for_model(Questions)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=question.id, text="Спасибо за информацию!")
    assert comment.content_object == question

@pytest.mark.django_db
def test_text_filled_correctly(user, review):
    """Тест: поле text заполнено корректно."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    assert comment.text == "Согласен с отзывом!"

@pytest.mark.django_db
def test_text_exceeds_max_length(user, review):
    """Тест: поле text превышает максимальную длину."""
    long_text = "x" * 201
    content_type = ContentType.objects.get_for_model(Reviews)
    with pytest.raises(ValidationError):
        comment = Comments(user_id=user, content_type=content_type, object_id=review.id, text=long_text)
        comment.full_clean()

@pytest.mark.django_db
def test_text_empty(user, review):
    """Тест: поле text не заполнено вызывает ValidationError."""
    content_type = ContentType.objects.get_for_model(Reviews)
    with pytest.raises(ValidationError):
        comment = Comments(user_id=user, content_type=content_type, object_id=review.id, text="")
        comment.full_clean()

@pytest.mark.django_db
def test_created_at_autofilled(user, review):
    """Тест: поле created_at заполняется автоматически."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    assert comment.created_at is not None

@pytest.mark.django_db
def test_str_method(user, review):
    """Тест: метод __str__ возвращает корректное значение."""
    content_type = ContentType.objects.get_for_model(Reviews)
    comment = Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")
    expected_str = f"{comment.user_id} {comment.text[:30]} {comment.content_object}"
    assert str(comment) == expected_str
