# import pytest
# from rest_framework.test import APIClient
# from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType
# from django.core.files.uploadedfile import SimpleUploadedFile
# import shutil
# from PIL import Image
# import io
# from .models import Categories, Places, PlacePhotos, Questions, Reviews, Comments, Votes

# User = get_user_model()


# def generate_test_image(color):
#     # Создание изображения 100x100 пикселей
#     image = Image.new('RGB', (100, 100), color=color)
#     buffer = io.BytesIO()
#     image.save(buffer, format='JPEG')
#     buffer.seek(0)
#     return SimpleUploadedFile(
#         "test_image.jpg",
#         buffer.read(),
#         content_type="image/jpeg"
#     )


# @pytest.fixture
# def api_client():
#     return APIClient()


# @pytest.fixture
# def admin_user():
#     return User.objects.create_superuser('admin@test.com', 'password')


# @pytest.fixture
# def regular_user():
#     return User.objects.create_user('user@test.com', 'password')


# @pytest.fixture
# def category():
#     return Categories.objects.create(name="Test Category")


# @pytest.fixture
# def place(category):
#     return Places.objects.create(name="Test Place", address="Test Street 1", category_id=category)


# @pytest.fixture
# def photo(place):
#     return PlacePhotos.objects.create(place_id=place, image=generate_test_image(color='blue'))


# @pytest.fixture
# def question(place, regular_user):
#     return Questions.objects.create(place_id=place, user_id=regular_user, text='Test Question')


# @pytest.fixture
# def review(place, regular_user):
#     return Reviews.objects.create(place_id=place, user_id=regular_user, text='Test Review', price=5, service=4, interior=5)


# @pytest.fixture
# def comment(regular_user, question):
#     content_type = ContentType.objects.get_for_model(question)
#     return Comments.objects.create(user_id=regular_user, content_object=question, content_type=content_type, object_id=question.id, text='Test Comment')


# @pytest.fixture
# def vote(regular_user, question):
#     content_type = ContentType.objects.get_for_model(question)
#     return Votes.objects.create(user_id=regular_user, content_object=question, content_type=content_type, object_id=question.id, vote_type=1)


# @pytest.mark.django_db
# class TestCategories:
#     def test_categories_view_access(self, api_client):
#         response = api_client.get('/review/categories/')
#         assert response.status_code == 200

#     def test_categories_add_by_admin(self, api_client, admin_user):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.post(
#             '/review/categories/', {'name': 'New Category'})
#         assert response.status_code == 201

#     def test_categories_add_by_regular_user(self, api_client, regular_user):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.post(
#             '/review/categories/', {'name': 'New Category'})
#         assert response.status_code == 403

#     def test_categories_update_by_admin(self, api_client, admin_user, category):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/categories/{category.id}/', {'name': 'Updated Category'})
#         assert response.status_code == 200

#     def test_categories_update_by_regular_user(self, api_client, regular_user, category):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/categories/{category.id}/', {'name': 'Updated Category'})
#         assert response.status_code == 403

#     def test_categories_delete_by_admin(self, api_client, admin_user, category):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/categories/{category.id}/')
#         assert response.status_code == 204

#     def test_categories_delete_by_regular_user(self, api_client, regular_user, category):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/categories/{category.id}/')
#         assert response.status_code == 403


# @pytest.mark.django_db
# class TestPlaces:
#     def test_places_view_access(self, api_client, place):
#         response = api_client.get('/review/places/')
#         assert response.status_code == 200

#     def test_places_add_by_admin(self, api_client, admin_user, category):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.post(
#             '/review/places/', {'name': 'New Place', 'address': 'New Address', 'category_id': category.id})
#         assert response.status_code == 201

#     def test_places_add_by_regular_user(self, api_client, regular_user, category):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.post(
#             '/review/places/', {'name': 'New Place', 'address': 'New Address', 'category_id': category.id})
#         assert response.status_code == 403

#     def test_places_update_by_admin(self, api_client, admin_user, place):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/places/{place.id}/', {'name': 'Updated Place'})
#         assert response.status_code == 200

#     def test_places_update_by_regular_user(self, api_client, regular_user, place):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/places/{place.id}/', {'name': 'Updated Place'})
#         assert response.status_code == 403

#     def test_places_delete_by_admin(self, api_client, admin_user, place):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/places/{place.id}/')
#         assert response.status_code == 204

#     def test_places_delete_by_regular_user(self, api_client, regular_user, place):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/places/{place.id}/')
#         assert response.status_code == 403


# @pytest.mark.django_db
# class TestPlacePhotos:
#     def test_photos_view_access(self, api_client, photo):
#         response = api_client.get('/review/place-photos/')
#         assert response.status_code == 200

#     def test_photos_add_by_admin(self, api_client, admin_user, place):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.post(
#             '/review/place-photos/', {'place_id': place.id, 'image': generate_test_image(color='red')}, format='multipart')
#         assert response.status_code == 201

#     def test_photos_add_by_regular_user(self, api_client, regular_user, place):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.post(
#             '/review/place-photos/', {'place_id': place.id, 'image': generate_test_image(color='red')}, format='multipart')
#         assert response.status_code == 403

#     def test_photos_update_by_admin(self, api_client, admin_user, photo):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/place-photos/{photo.id}/', {'image': generate_test_image(color='green')}, format='multipart')
#         assert response.status_code == 200

#     def test_photos_update_by_regular_user(self, api_client, regular_user, photo):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/place-photos/{photo.id}/', {'image': generate_test_image(color='green')}, format='multipart')
#         assert response.status_code == 403

#     def test_photos_delete_by_admin(self, api_client, admin_user, photo):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/place-photos/{photo.id}/')
#         assert response.status_code == 204

#     def test_photos_delete_by_regular_user(self, api_client, regular_user, photo):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/place-photos/{photo.id}/')
#         assert response.status_code == 403


# @pytest.mark.django_db
# class TestQuestions:
#     def test_questions_view_access(self, api_client, question):
#         response = api_client.get('/review/questions/')
#         assert response.status_code == 200

#     def test_questions_add_by_authenticated_user(self, api_client, regular_user, place):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.post(
#             '/review/questions/', {'place_id': place.id, 'user_id': regular_user.id, 'text': 'New Question'})
#         assert response.status_code == 201

#     def test_questions_add_by_anonymous_user(self, api_client, place):
#         response = api_client.post(
#             '/review/questions/', {'place_id': place.id, 'text': 'New Question'})
#         assert response.status_code == 401

#     def test_questions_update_by_owner(self, api_client, regular_user, question):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/questions/{question.id}/', {'text': 'Updated Question'})
#         assert response.status_code == 200

#     def test_questions_update_by_other_user(self, api_client, admin_user, question):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/questions/{question.id}/', {'text': 'Updated Question'})
#         assert response.status_code == 403

#     def test_questions_delete_by_admin(self, api_client, admin_user, question):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/questions/{question.id}/')
#         assert response.status_code == 204

#     def test_questions_delete_by_owner(self, api_client, regular_user, question):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/questions/{question.id}/')
#         assert response.status_code == 403


# @pytest.mark.django_db
# class TestReviews:
#     def test_reviews_view_access(self, api_client, review):
#         response = api_client.get('/review/reviews/')
#         assert response.status_code == 200

#     def test_reviews_add_by_authenticated_user(self, api_client, regular_user, place):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.post('/review/reviews/', {
#             'place_id': place.id, 'user_id': regular_user.id, 'text': 'New Review', 'price': 4, 'service': 5, 'interior': 3
#         })
#         assert response.status_code == 201

#     def test_reviews_add_by_anonymous_user(self, api_client, place):
#         response = api_client.post('/review/reviews/', {
#             'place_id': place.id, 'text': 'New Review', 'price': 4, 'service': 5, 'interior': 3
#         })
#         assert response.status_code == 401

#     def test_reviews_update_by_owner(self, api_client, regular_user, review):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/reviews/{review.id}/', {'text': 'Updated Review'})
#         assert response.status_code == 200

#     def test_reviews_update_by_other_user(self, api_client, admin_user, review):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/reviews/{review.id}/', {'text': 'Updated Review'})
#         assert response.status_code == 403

#     def test_reviews_delete_by_admin(self, api_client, admin_user, review):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/reviews/{review.id}/')
#         assert response.status_code == 204

#     def test_reviews_delete_by_owner(self, api_client, regular_user, review):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/reviews/{review.id}/')
#         assert response.status_code == 403


# @pytest.mark.django_db
# class TestComments:
#     def test_comments_view_access(self, api_client, comment):
#         response = api_client.get('/review/comments/')
#         assert response.status_code == 200
#         assert isinstance(response.data[0]['content_object'], str)

#     def test_comments_add_by_authenticated_user(self, api_client, regular_user, question):
#         api_client.force_authenticate(user=regular_user)
#         content_type = ContentType.objects.get_for_model(question)
#         response = api_client.post('/review/comments/', {
#             'object_id': question.id, 'user_id': regular_user.id, 'content_type': content_type.id, 'text': 'New Comment'
#         })
#         assert response.status_code == 201

#     def test_comments_add_by_anonymous_user(self, api_client, question):
#         content_type = ContentType.objects.get_for_model(question)
#         response = api_client.post('/review/comments/', {
#             'object_id': question.id, 'content_type': content_type.id, 'text': 'New Comment'
#         })
#         assert response.status_code == 401

#     def test_comments_update_by_owner(self, api_client, regular_user, comment):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/comments/{comment.id}/', {'text': 'Updated Comment'})
#         assert response.status_code == 200

#     def test_comments_update_by_other_user(self, api_client, admin_user, comment):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/comments/{comment.id}/', {'text': 'Updated Comment'})
#         assert response.status_code == 403

#     def test_comments_delete_by_admin(self, api_client, admin_user, comment):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/comments/{comment.id}/')
#         assert response.status_code == 204

#     def test_comments_delete_by_owner(self, api_client, regular_user, comment):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/comments/{comment.id}/')
#         assert response.status_code == 403


# @pytest.mark.django_db
# class TestVotes:
#     def test_votes_view_access(self, api_client, vote):
#         response = api_client.get('/review/votes/')
#         assert response.status_code == 200
#         assert isinstance(response.data[0]['content_object'], str)

#     def test_votes_add_by_authenticated_user(self, api_client, regular_user, question):
#         content_type = ContentType.objects.get_for_model(question)
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.post('/review/votes/', {
#             'object_id': question.id, 'user_id': regular_user.id, 'content_type': content_type.id, 'vote_type': 1
#         })
#         assert response.status_code == 201

#     def test_votes_add_by_anonymous_user(self, api_client, question):
#         content_type = ContentType.objects.get_for_model(question)
#         response = api_client.post('/review/votes/', {
#             'object_id': question.id, 'content_type': content_type.id, 'vote_type': 1
#         })
#         assert response.status_code == 401

#     def test_votes_update_by_owner(self, api_client, regular_user, vote):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.patch(
#             f'/review/votes/{vote.id}/', {'vote_type': -1})
#         assert response.status_code == 200

#     def test_votes_update_by_other_user(self, api_client, admin_user, vote):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.patch(
#             f'/review/votes/{vote.id}/', {'vote_type': -1})
#         assert response.status_code == 403

#     def test_votes_delete_by_admin(self, api_client, admin_user, vote):
#         api_client.force_authenticate(user=admin_user)
#         response = api_client.delete(f'/review/votes/{vote.id}/')
#         assert response.status_code == 204

#     def test_votes_delete_by_owner(self, api_client, regular_user, vote):
#         api_client.force_authenticate(user=regular_user)
#         response = api_client.delete(f'/review/votes/{vote.id}/')
#         assert response.status_code == 204


# @pytest.fixture(scope='function', autouse=True)
# def cleanup_media():
#     yield
#     shutil.rmtree('images/', ignore_errors=True)
