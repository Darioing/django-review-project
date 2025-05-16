import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from reviews.models import Questions

pytestmark = pytest.mark.django_db


def test_list_questions_unauthenticated(api_client, create_category, create_place, create_question, normal_user):
    cat = create_category(name='CatQ', slug='catq')
    place = create_place(category=cat)
    # Создание вопросов
    create_question(place=place, user=normal_user, text='Q1')
    create_question(place=place, user=normal_user, text='Q2')
    url = reverse('reviews:question-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    texts = {q['text'] for q in response.data}
    assert {'Q1', 'Q2'} <= texts


def test_filter_questions_by_place(api_client, create_category, create_place, create_question, normal_user):
    cat = create_category(name='CatFilter', slug='filter-cat')
    place1 = create_place(name='Place1', slug='p1', category=cat)
    place2 = create_place(name='Place2', slug='p2', category=cat)
    create_question(place=place1, user=normal_user, text='ForPlace1')
    create_question(place=place2, user=normal_user, text='ForPlace2')
    url = reverse('reviews:question-list') + f'?place_id={place1.id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['text'] == 'ForPlace1'


def test_retrieve_question(api_client, create_category, create_place, create_question):
    cat = create_category(name='CatDetail', slug='detail-cat')
    place = create_place(category=cat)
    question = create_question(place=place, text='DetailQ')
    url = reverse('reviews:question-detail', args=[question.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == question.id
    assert response.data['text'] == 'DetailQ'
    assert 'user_fio' in response.data
    assert 'self_content_type' in response.data
    assert 'comment_count' in response.data


def test_create_question_unauthenticated(api_client, create_category, create_place):
    cat = create_category(name='CatNew', slug='new-cat')
    place = create_place(category=cat)
    url = reverse('reviews:question-list')
    data = {'place_id': place.id, 'text': 'NewQ'}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_question_authenticated(auth_api_client, normal_user, create_category, create_place):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatAuth', slug='auth-cat')
    place = create_place(category=cat)
    url = reverse('reviews:question-list')
    data = {'place_id': place.id, 'text': 'AuthQ', 'user_id': normal_user.id}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == 'AuthQ'
    assert response.data['user_id'] == normal_user.id
    ct = ContentType.objects.get_for_model(Questions)
    assert response.data['self_content_type'] == ct.id


def test_update_question_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_question, create_user):
    cat = create_category(name='CatUpd', slug='upd-cat')
    place = create_place(category=cat)
    # Вопрос от normal_user
    question = create_question(place=place, user=normal_user, text='Orig')
    url = reverse('reviews:question-detail', args=[question.id])
    # другой пользователь
    other = create_user(email='other@example.com')
    auth_api_client.force_authenticate(user=other)
    resp = auth_api_client.patch(url, {'text': 'Updated'})
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # владелец
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.patch(url, {'text': 'Updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['text'] == 'Updated'


def test_delete_question_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_question):
    cat = create_category(name='CatDel', slug='del-cat')
    place = create_place(category=cat)
    question = create_question(place=place, user=normal_user)
    url = reverse('reviews:question-detail', args=[question.id])
    # владелец не может удалить
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # администратор может удалить
    auth_api_client.force_authenticate(user=staff_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
