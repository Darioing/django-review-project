import pytest

from django.db.utils import IntegrityError

from reviews.models import PlacePhotos, Places


@pytest.fixture
def place():
    """Фикстура для создания объекта Places."""
    return Places.objects.create(name="Кафе", address="ул. Ленина, 1", category_id=None)


@pytest.mark.django_db
def test_place_id_filled_correctly(place):
    """Тест: поле place_id заполнено корректно."""
    photo = PlacePhotos.objects.create(
        place_id=place, image="images/photo.PNG")
    assert photo.place_id == place


@pytest.mark.django_db
def test_place_id_empty():
    """Тест: поле place_id не заполнено вызывает IntegrityError."""
    with pytest.raises(IntegrityError):
        PlacePhotos.objects.create(place_id=None, image="images/photo.PNG")


@pytest.mark.django_db
def test_place_deletion_cascades_to_photos(place):
    """Тест: при удалении place удаляются связанные фотографии."""
    photo = PlacePhotos.objects.create(
        place_id=place, image="images/photo.PNG")
    place.delete()
    assert PlacePhotos.objects.all().count() == 0


@pytest.mark.django_db
def test_image_filled_correctly(place):
    """Тест: поле image заполнено корректно."""
    photo = PlacePhotos.objects.create(
        place_id=place, image="images/photo.PNG")
    assert photo.image.name == "images/photo.PNG"


@pytest.mark.django_db
def test_str_method(place):
    """Тест: метод __str__ возвращает значение place_id корректно."""
    photo = PlacePhotos.objects.create(
        place_id=place, image="images/photo.PNG")
    assert photo.__str__() == place
