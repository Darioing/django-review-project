from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("review/", include("reviews.urls")),
    path("user/", include("reviews.urls")),
    path('admin/', admin.site.urls),
]
