import pytest
from reviews.models import Votes, Reviews, Questions, Comments, Places
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

@pytest.fixture
def comment(user, review):
    """Фикстура для создания объекта Comments."""
    content_type = ContentType.objects.get_for_model(Reviews)
    return Comments.objects.create(user_id=user, content_type=content_type, object_id=review.id, text="Согласен с отзывом!")

@pytest.mark.django_db
def test_user_id_filled_correctly(user, review):
    """Тест: поле user_id заполнено корректно."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    assert vote.user_id == user

@pytest.mark.django_db
def test_user_id_empty(review):
    """Тест: поле user_id не заполнено вызывает IntegrityError."""
    content_type = ContentType.objects.get_for_model(Reviews)
    with pytest.raises(IntegrityError):
        Votes.objects.create(user_id=None, content_type=content_type, object_id=review.id, vote_type=1)

@pytest.mark.django_db
def test_user_deletion_cascades_to_votes(user, review):
    """Тест: при удалении user удаляется и vote."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    user.delete()
    assert Votes.objects.all().count() == 0

@pytest.mark.django_db
def test_content_type_reviews(user, review):
    """Тест: поле content_type заполняется типом объекта reviews."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    assert vote.content_type == content_type

@pytest.mark.django_db
def test_object_id_reviews(user, review):
    """Тест: поле object_id заполнено корректно существующим объектом reviews."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    assert vote.object_id == review.id

@pytest.mark.django_db
def test_content_object_reviews(user, review):
    """Тест: поле content_object заполняется корректно."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    assert vote.content_object == review

@pytest.mark.django_db
def test_content_type_questions(user, question):
    """Тест: поле content_type заполняется типом объекта questions."""
    content_type = ContentType.objects.get_for_model(Questions)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=question.id, vote_type=1)
    assert vote.content_type == content_type

@pytest.mark.django_db
def test_object_id_questions(user, question):
    """Тест: поле object_id заполнено корректно существующим объектом question."""
    content_type = ContentType.objects.get_for_model(Questions)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=question.id, vote_type=1)
    assert vote.object_id == question.id

@pytest.mark.django_db
def test_content_object_questions(user, question):
    """Тест: поле content_object заполняется корректно."""
    content_type = ContentType.objects.get_for_model(Questions)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=question.id, vote_type=1)
    assert vote.content_object == question

@pytest.mark.django_db
def test_content_type_comments(user, comment):
    """Тест: поле content_type заполняется типом объекта comment."""
    content_type = ContentType.objects.get_for_model(Comments)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=comment.id, vote_type=1)
    assert vote.content_type == content_type

@pytest.mark.django_db
def test_object_id_comments(user, comment):
    """Тест: поле object_id заполнено корректно существующим объектом comment."""
    content_type = ContentType.objects.get_for_model(Comments)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=comment.id, vote_type=1)
    assert vote.object_id == comment.id

@pytest.mark.django_db
def test_content_object_comments(user, comment):
    """Тест: поле content_object заполняется корректно."""
    content_type = ContentType.objects.get_for_model(Comments)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=comment.id, vote_type=1)
    assert vote.content_object == comment

@pytest.mark.django_db
def test_vote_type_upvote(user, review):
    """Тест: поле vote_type заполнено значением 1."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    assert vote.vote_type == 1

@pytest.mark.django_db
def test_vote_type_downvote(user, review):
    """Тест: поле vote_type заполнено значением -1."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=-1)
    assert vote.vote_type == -1

@pytest.mark.django_db
def test_vote_type_invalid(user, review):
    """Тест: поле vote_type заполнено некорректным значением вызывает ValidationError."""
    content_type = ContentType.objects.get_for_model(Reviews)
    with pytest.raises(ValidationError):
        vote = Votes(user_id=user, content_type=content_type, object_id=review.id, vote_type=2)
        vote.full_clean()

@pytest.mark.django_db
def test_created_at_autofilled(user, review):
    """Тест: поле created_at заполняется автоматически."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    assert vote.created_at is not None

@pytest.mark.django_db
def test_str_method(user, review):
    """Тест: метод __str__ возвращает корректное значение."""
    content_type = ContentType.objects.get_for_model(Reviews)
    vote = Votes.objects.create(user_id=user, content_type=content_type, object_id=review.id, vote_type=1)
    expected_str = f"{vote.user_id} оставил {vote.vote_type} к {vote.content_object}"
    assert str(vote) == expected_str
