from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, Sum
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
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
    filter_backends = [DjangoFilterBackend]


class PlacesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Places
        fields = ['name']

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class PlacesViewSet(viewsets.ModelViewSet):
    queryset = Places.objects.prefetch_related(
        'photos'
    ).annotate(review_count=Count('reviews'))
    serializer_class = PlacesSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_class = PlacesFilter  # Используем кастомный фильтр


class PlacePhotosViewSet(viewsets.ModelViewSet):
    queryset = PlacePhotos.objects.all()
    serializer_class = PlacePhotosSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.none()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticatedToCreate]
    filter_backends = [DjangoFilterBackend]

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
    filter_backends = [DjangoFilterBackend]

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
    filter_backends = [DjangoFilterBackend]

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

        try:
            model_content_type = ContentType.objects.get(pk=content_type)
        except ContentType.DoesNotExist:
            return Response({"error": "Неверный content_type"}, status=400)
        # Фильтруем комментарии по content_type и object_id
        comments = Comments.objects.filter(
            content_type=model_content_type,
            object_id=pk
        )
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class VotesViewSet(viewsets.ModelViewSet):
    queryset = Votes.objects.all()
    serializer_class = VotesSerializer
    permission_classes = [IsAuthenticatedToCreate]
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        user = request.user
        content_type_id = request.data.get('content_type')
        object_id = request.data.get('object_id')
        vote_type = int(request.data.get('vote_type'))

        try:
            content_type = ContentType.objects.get(id=content_type_id)
            existing_vote = Votes.objects.filter(
                user_id=user,
                content_type=content_type,
                object_id=object_id
            ).first()

            if existing_vote:
                # Если голос существует, обновляем его
                existing_vote.vote_type = vote_type
                existing_vote.save()
            else:
                # Если голоса нет, создаём новый
                Votes.objects.create(
                    user_id=user,
                    content_type=content_type,
                    object_id=object_id,
                    vote_type=vote_type
                )

            # Пересчитываем сумму голосов для объекта
            total_votes = Votes.objects.filter(
                content_type=content_type,
                object_id=object_id
            ).aggregate(total=Sum('vote_type'))['total'] or 0

            return Response(
                {"detail": "Vote processed successfully",
                    "total_votes": total_votes},
                status=status.HTTP_200_OK
            )
        except ContentType.DoesNotExist:
            raise ValidationError({"content_type": "Invalid content type"})

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='total-votes')
    def total_votes(self, request):
        """Получение общей суммы голосов для конкретного объекта."""
        content_type = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')
        if not content_type or not object_id:
            return Response(
                {"error": "content_type и object_id обязательны"},
                status=400
            )

        try:
            model_content_type = ContentType.objects.get(pk=content_type)
        except ContentType.DoesNotExist:
            return Response({"error": "Неверный content_type"}, status=400)

        total_votes = Votes.objects.filter(
            content_type=model_content_type,
            object_id=object_id
        ).aggregate(total=Sum('vote_type'))['total'] or 0

        return Response({"total_votes": total_votes})

    @action(detail=False, methods=['get'], url_path='user-vote', permission_classes=[IsAuthenticated])
    def user_vote(self, request):
        """Получение текущего голоса пользователя для объекта."""
        content_type = request.query_params.get('content_type')
        object_id = request.query_params.get('object_id')
        if not content_type or not object_id:
            return Response(
                {"error": "content_type и object_id обязательны"},
                status=400
            )

        try:
            model_content_type = ContentType.objects.get(pk=content_type)
        except ContentType.DoesNotExist:
            return Response({"error": "Неверный content_type"}, status=400)

        vote = Votes.objects.filter(
            content_type=model_content_type,
            object_id=object_id,
            user_id=request.user
        ).first()

        return Response({"user_vote": vote.vote_type if vote else 0})
