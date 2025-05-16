from rest_framework.routers import DefaultRouter
from .views import (
    CategoriesViewSet,
    PlacesViewSet,
    PlacePhotosViewSet,
    QuestionsViewSet,
    ReviewsViewSet,
    CommentsViewSet,
    VotesViewSet,
)

app_name = 'reviews'

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='category')
router.register(r'places', PlacesViewSet, basename='place')
router.register(r'place-photos', PlacePhotosViewSet, basename='place-photo')
router.register(r'questions', QuestionsViewSet, basename='question')
router.register(r'reviews', ReviewsViewSet, basename='review')
router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'votes', VotesViewSet, basename='vote')

urlpatterns = router.urls
