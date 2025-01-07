from django.contrib import admin

from .models import Categories, Places, PlacePhotos, Questions, Reviews, Comments, Votes


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
    ]
    list_filter = [
        'name',
    ]
    readonly_fields = ('slug',)


@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'address',
        'category_id',
        'about',
        'rating',
        'slug',
    ]
    list_filter = [
        'name',
        'address',
    ]
    readonly_fields = ('slug', 'rating')


@admin.register(PlacePhotos)
class PlacePhotosAdmin(admin.ModelAdmin):
    list_display = [
        'place_id',
        'image',
    ]
    list_filter = [
        'place_id',
    ]


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = [
        'place_id',
        'user_id',
        'text',
        'price',
        'service',
        'interior',
        'created_at',
    ]
    list_filter = [
        'place_id',
        'text',
    ]


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = [
        'place_id',
        'user_id',
        'text',
        'created_at',
    ]
    list_filter = [
        'place_id',
        'text',
    ]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = [
        'user_id',
        'content_type',
        'object_id',
        'content_object',
        'text',
        'created_at',
    ]
    list_filter = [
        'user_id',
        'text',
    ]


@admin.register(Votes)
class VotesAdmin(admin.ModelAdmin):
    list_display = [
        'user_id',
        'content_type',
        'object_id',
        'content_object',
        'vote_type',
        'created_at',
    ]
    list_filter = [
        'user_id',
    ]
