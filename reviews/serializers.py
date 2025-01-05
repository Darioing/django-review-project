from rest_framework import serializers
from .models import Categories, Places, PlacePhotos, Questions, Reviews, Comments, Votes


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Places
        fields = ['id', 'name', 'address', 'category_id', 'slug']
        read_only_fields = ['slug']


class PlacePhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacePhotos
        fields = ['id', 'place_id', 'image']


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'place_id', 'user_id', 'text', 'created_at']
        read_only_fields = ['created_at']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            'id', 'place_id', 'user_id', 'text', 'price', 'service',
            'interior', 'created_at'
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
