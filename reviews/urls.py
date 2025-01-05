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
router.register(r'categories', CategoriesViewSet)
router.register(r'places', PlacesViewSet)
router.register(r'place-photos', PlacePhotosViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'reviews', ReviewsViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'votes', VotesViewSet)

urlpatterns = router.urls
