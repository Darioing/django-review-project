import pytest
import django
from django.conf import settings
from django.urls import reverse, resolve

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType

from reviews.models import Categories, Places, PlacePhotos, Questions, Reviews, Comments, Votes


def pytest_configure():
    django.setup()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    User = get_user_model()

    def make_user(**kwargs):
        user = User.objects.create_user(
            email=kwargs.get('email', 'test@example.com'),
            password=kwargs.get('password', 'testpass123'),
            FIO=kwargs.get('FIO', 'Test User')
        )
        return user
    return make_user


@pytest.fixture
def normal_user(create_user):
    return create_user(email='user@example.com', password='userpass', FIO='Normal User')


@pytest.fixture
def staff_user(create_user):
    user = create_user(email='staff@example.com',
                       password='staffpass', FIO='Staff User')
    user.is_staff = True
    user.save()
    return user


@pytest.fixture
def auth_api_client(api_client):
    """
    Возвращает APIClient, не аутентифицированный по умолчанию.
    Для аутентификации используйте метод force_authenticate в тестах.
    """
    return api_client


# Factory fixtures for models
@pytest.fixture
def create_category(db):
    def make_category(**kwargs):
        return Categories.objects.create(
            name=kwargs.get('name', 'Test Category'),
            slug=kwargs.get('slug', 'test-category')
        )
    return make_category


@pytest.fixture
def category(create_category):
    return create_category(name='Simple Name', slug='simple-name')


@pytest.fixture
def create_place(db, create_category):
    def make_place(**kwargs):
        category = kwargs.get('category') or create_category()
        return Places.objects.create(
            name=kwargs.get('name', 'Test Place'),
            address=kwargs.get('address', '123 Main St'),
            category_id=category,
            about=kwargs.get('about', 'About text')
        )
    return make_place


@pytest.fixture
def place(create_place, create_category):
    category = create_category(name='Cafe', slug='cafe')
    return create_place(name='Central Cafe', address='City Center', category=category, about='A cozy place')


@pytest.fixture
def create_placephoto(create_place):
    def make_placephoto(**kwargs):
        place_instance = kwargs.pop('place_id', None) or create_place()
        placephoto = PlacePhotos.objects.create(
            place_id=place_instance, **kwargs)
        return placephoto
    return make_placephoto


@pytest.fixture
def placephoto(create_placephoto, place):
    # В качестве image используем простой ContentFile
    from django.core.files.base import ContentFile
    image_file = ContentFile(b'mock image data', name='test.jpg')
    return create_placephoto(place_id=place, image=image_file)


@pytest.fixture
def create_question(db, create_place, create_user):
    def make_question(**kwargs):
        place = kwargs.get('place') or create_place()
        user = kwargs.get('user') or create_user()
        return Questions.objects.create(
            place_id=place,
            user_id=user,
            text=kwargs.get('text', 'Test question')
        )
    return make_question


@pytest.fixture
def question(create_question, place, create_user):
    user = create_user(email='asker@example.com', FIO='Asker')
    return create_question(place=place, user=user, text='Do you have vegan options?')


@pytest.fixture
def create_review(db, create_place, create_user):
    def make_review(**kwargs):
        place = kwargs.get('place') or create_place()
        user = kwargs.get('user') or create_user()
        return Reviews.objects.create(
            place_id=place,
            user_id=user,
            text=kwargs.get('text', 'Test review'),
            price=kwargs.get('price', 5),
            service=kwargs.get('service', 5),
            interior=kwargs.get('interior', 5)
        )
    return make_review


@pytest.fixture
def review(create_review, place, normal_user):
    return create_review(
        place=place,
        user=normal_user,
        text='Nice food and ambiance',
        price=4,
        service=5,
        interior=4
    )


@pytest.fixture
def create_comment(db, create_review, create_user):
    def make_comment(**kwargs):
        user = kwargs.get('user') or create_user()
        content_type = kwargs.get('content_type')
        object_id = kwargs.get('object_id')
        if not content_type or not object_id:
            review = kwargs.get('review') or create_review(user=user)
            content_type = ContentType.objects.get_for_model(review)
            object_id = review.id
        return Comments.objects.create(
            user_id=user,
            content_type=content_type,
            object_id=object_id,
            text=kwargs.get('text', 'Test comment')
        )
    return make_comment


@pytest.fixture
def comment(create_comment, review, create_user):
    from django.contrib.contenttypes.models import ContentType
    user = create_user(email='commenter@example.com', FIO='Commenter')
    content_type = ContentType.objects.get_for_model(review)
    return create_comment(user=user, content_type=content_type, object_id=review.id, text='Agree with this review')


@pytest.fixture
def create_vote(db, create_review, create_user):
    def make_vote(**kwargs):
        user = kwargs.get('user') or create_user()
        review = kwargs.get('review') or create_review(user=user)
        content_type = ContentType.objects.get_for_model(review)
        return Votes.objects.create(
            user_id=user,
            content_type=content_type,
            object_id=review.id,
            vote_type=kwargs.get('vote_type', 1)
        )
    return make_vote


@pytest.fixture
def vote(create_vote, review, create_user):
    return create_vote(user=create_user(email='voter@example.com', FIO='Voter'), review=review, vote_type=1)


@pytest.fixture
def admin_api_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client
