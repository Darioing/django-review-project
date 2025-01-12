from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsAuthenticatedToCreate
from .models import Categories, Places, PlacePhotos, Questions, Reviews, Comments, Votes
from .serializers import (
    CategoriesSerializer,
    PlacesSerializer,
    PlacePhotosSerializer,
    QuestionsSerializer,
    ReviewsSerializer,
    CommentsSerializer,
    VotesSerializer
)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]


class PlacesViewSet(viewsets.ModelViewSet):
    queryset = Places.objects.prefetch_related(
        'photos').all()  # Оптимизация запросов
    serializer_class = PlacesSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"  # Указываем поле для поиска

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        place = get_object_or_404(Places, slug=slug)
        serializer = self.get_serializer(place, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return super().get_queryset().annotate(review_count=Count('reviews'))


class PlacePhotosViewSet(viewsets.ModelViewSet):
    queryset = PlacePhotos.objects.all()
    serializer_class = PlacePhotosSerializer
    permission_classes = [IsAdminOrReadOnly]


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.none()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticatedToCreate]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Questions.objects.all()
        # Получение параметра place_id из запроса
        place_id = self.request.query_params.get('place_id')
        if place_id:
            # Фильтрация по place_id
            queryset = queryset.filter(place_id=place_id)
        return queryset


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedToCreate]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='by-place/(?P<place_id>[^/.]+)')
    def by_place(self, request, place_id=None):
        reviews = self.queryset.filter(place_id=place_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedToCreate]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()

    @action(detail=True, methods=["get"], url_path="by-object")
    def by_object(self, request, pk=None):
        # Получаем параметр content_type из запроса
        content_type = request.query_params.get('content_type')
        if not content_type:
            return Response({"error": "Content type is required."}, status=400)

        # Фильтруем комментарии по content_type и object_id
        comments = Comments.objects.filter(
            content_type=content_type,
            object_id=pk
        )
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class VotesViewSet(viewsets.ModelViewSet):
    queryset = Votes.objects.all()
    serializer_class = VotesSerializer
    permission_classes = [IsAuthenticatedToCreate]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwnerOrReadOnly]
        return super().get_permissions()
