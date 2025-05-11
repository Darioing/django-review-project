from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    ProtectedView,
    LogoutView,
)
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, VerifyEmailView

app_name = 'users'

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/<str:token>/',
         VerifyEmailView.as_view(), name='verify-email'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', CustomTokenObtainPairView.as_view(), name='custom_login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls
