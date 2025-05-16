import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db
def test_create_comment_without_text(admin_api_client, normal_user, create_question):
    question = create_question()
    content_type = ContentType.objects.get_for_model(question)
    url = reverse('reviews:comments-list')
    data = {
        'user_id': normal_user.id,
        'content_type': content_type.id,
        'object_id': question.id,
        'text': ''
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'text' in response.data


@pytest.mark.django_db
def test_create_comment_with_invalid_content_object(admin_api_client, normal_user):
    url = reverse('reviews:comments-list')
    data = {
        'user_id': normal_user.id,
        'content_type': 999,  # Не существующий content_type
        'object_id': 1,
        'text': 'Test comment'
    }
    response = admin_api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
