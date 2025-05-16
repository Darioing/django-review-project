import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

from reviews.models import Comments, Questions, Reviews

pytestmark = pytest.mark.django_db


def test_list_comments_unauthenticated(api_client, create_comment, create_category, create_place, create_review, normal_user):
    # Создание комментариев к отзыву
    cat = create_category(name='CatC', slug='catc')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    create_comment(user=normal_user, content_type=ContentType.objects.get_for_model(
        review), object_id=review.id, text='C1')
    create_comment(user=normal_user, content_type=ContentType.objects.get_for_model(
        review), object_id=review.id, text='C2')
    url = reverse('reviews:comments-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    texts = {c['text'] for c in response.data}
    assert {'C1', 'C2'} <= texts


def test_by_object_action(api_client, create_comment, create_category, create_place, create_review, normal_user):
    cat = create_category(name='CatCO', slug='cato')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    ct = ContentType.objects.get_for_model(review)
    # комментарии к разным объектам
    create_comment(user=normal_user, content_type=ct,
                   object_id=review.id, text='ForObj1')
    # комментарий к несуществующему объекту
    create_comment(user=normal_user, content_type=ct,
                   object_id=review.id+1, text='Other')
    url = reverse('reviews:comments-by-object',
                  args=[review.id]) + f'?content_type={ct.id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['text'] == 'ForObj1'


def test_retrieve_comment(api_client, create_comment, create_category, create_place, create_review, normal_user):
    cat = create_category(name='CatDetailC', slug='detailc')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    comment = create_comment(user=normal_user, content_type=ContentType.objects.get_for_model(
        review), object_id=review.id, text='DetailC')
    url = reverse('reviews:comments-detail', args=[comment.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == comment.id
    assert response.data['text'] == 'DetailC'
    assert 'user_fio' in response.data
    assert 'self_content_type' in response.data
    assert 'children' in response.data


def test_create_comment_unauthenticated(api_client, create_category, create_place, create_review):
    cat = create_category(name='CatNewC', slug='newc')
    place = create_place(category=cat)
    review = create_review(place=place)
    url = reverse('reviews:comments-list')
    data = {'content_type': ContentType.objects.get_for_model(
        review).id, 'object_id': review.id, 'text': 'NewC'}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_comment_authenticated(auth_api_client, normal_user, create_category, create_place, create_review):
    auth_api_client.force_authenticate(user=normal_user)
    cat = create_category(name='CatAuthC', slug='authc')
    place = create_place(category=cat)
    review = create_review(place=place)
    ct = ContentType.objects.get_for_model(review)
    url = reverse('reviews:comments-list')
    data = {'user_id': normal_user.id, 'content_type': ct.id,
            'object_id': review.id, 'text': 'AuthC'}
    response = auth_api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == 'AuthC'
    assert response.data['user_id'] == normal_user.id
    assert response.data['text'] == 'AuthC'
    assert response.data['user_id'] == normal_user.id


def test_update_comment_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_review, create_comment):
    cat = create_category(name='CatUpdC', slug='updc')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    comment = create_comment(user=normal_user, content_type=ContentType.objects.get_for_model(
        review), object_id=review.id)
    url = reverse('reviews:comments-detail', args=[comment.id])
    # другой пользователь
    other = normal_user.__class__.objects.create_user(
        email='other3@example.com', password='pass')
    auth_api_client.force_authenticate(user=other)
    resp = auth_api_client.patch(url, {'text': 'Updated'})
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # владелец может изменить
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.patch(url, {'text': 'Updated'})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['text'] == 'Updated'


def test_delete_comment_permissions(auth_api_client, normal_user, staff_user, create_category, create_place, create_review, create_comment):
    cat = create_category(name='CatDelC', slug='delc')
    place = create_place(category=cat)
    review = create_review(place=place, user=normal_user)
    comment = create_comment(user=normal_user, content_type=ContentType.objects.get_for_model(
        review), object_id=review.id)
    url = reverse('reviews:comments-detail', args=[comment.id])
    # валдевец не может удалить
    auth_api_client.force_authenticate(user=normal_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # администратор может удалить
    auth_api_client.force_authenticate(user=staff_user)
    resp = auth_api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
