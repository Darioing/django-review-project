from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'FIO',
        'email',
        'image',
    ]
    list_filter = [
        'email',
    ]
