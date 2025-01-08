from rest_framework import serializers
from .models import Categories, Places, PlacePhotos, Questions, Reviews, Comments, Votes


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class PlacesSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    review_count = serializers.IntegerField(read_only=True)
    category_name = serializers.ReadOnlyField(
        source="category_id.name")  # Получаем имя категории

    class Meta:
        model = Places
        fields = ['id', 'name', 'address',
                  'category_id', 'about', 'slug', 'photos', 'rating', 'category_name', 'review_count']
        read_only_fields = ['slug', 'rating',]

    def get_photos(self, obj):
        # Получаем список всех связанных фотографий
        all_photos = obj.photos.all()
        request = self.context.get('request')  # Получение контекста запроса
        if all_photos:
            # Возвращаем список URL фотографий
            return [request.build_absolute_uri(photo.image.url) for photo in all_photos]
        return []


class PlacePhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacePhotos
        fields = ['id', 'place_id', 'image']


class QuestionsSerializer(serializers.ModelSerializer):
    user_fio = serializers.ReadOnlyField(
        source='user_id.FIO')  # Полное имя пользователя
    user_avatar = serializers.ImageField(
        source='user_id.image', read_only=True)  # Аватар пользователя

    class Meta:
        model = Questions
        fields = ['id', 'place_id', 'user_id', 'text',
                  'created_at', 'user_fio', 'user_avatar']
        read_only_fields = ['created_at']


class ReviewsSerializer(serializers.ModelSerializer):
    user_fio = serializers.ReadOnlyField(
        source='user_id.FIO')  # Полное имя пользователя
    user_avatar = serializers.ImageField(
        source='user_id.image', read_only=True)  # Аватар пользователя

    class Meta:
        model = Reviews
        fields = [
            'id', 'place_id', 'user_id', 'text', 'price', 'service',
            'interior', 'created_at', 'user_fio', 'user_avatar',
        ]
        read_only_fields = ['created_at']


class CommentsSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = [
            'id', 'user_id', 'content_type', 'object_id', 'content_object',
            'text', 'created_at'
        ]
        read_only_fields = ['created_at', 'content_object']

    def get_content_object(self, obj):
        # Возвращаем строковое представление связанного объекта
        return str(obj.content_object)


class VotesSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Votes
        fields = [
            'id', 'user_id', 'content_type', 'object_id', 'content_object',
            'vote_type', 'created_at'
        ]
        read_only_fields = ['created_at', 'content_object']

    def get_content_object(self, obj):
        # Возвращает строковое представление связанного объекта
        return str(obj.content_object)
