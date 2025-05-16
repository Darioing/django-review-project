import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db
def test_create_question_with_duplicate_text(admin_api_client, normal_user, create_place):
    place = create_place()
    url = reverse('reviews:question-list')
    data = {
        'user_id': normal_user.id,
        'place_id': place.id,
        'text': 'How late is the place open?'
    }
    # первый запрос — успешен
    response1 = admin_api_client.post(url, data)
    assert response1.status_code == status.HTTP_201_CREATED
    # второй запрос — дубликат, ошибка
    response2 = admin_api_client.post(url, data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response2.data
