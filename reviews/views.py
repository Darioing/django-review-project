from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
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
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    permission_classes = [IsAdminOrReadOnly]


class PlacePhotosViewSet(viewsets.ModelViewSet):
    queryset = PlacePhotos.objects.all()
    serializer_class = PlacePhotosSerializer
    permission_classes = [IsAdminOrReadOnly]


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticatedToCreate]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrReadOnly]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminOrReadOnly]
        return super().get_permissions()


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
