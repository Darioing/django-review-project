from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Доступ к чтению для всех
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Изменение доступно только владельцу
        return obj == request.user
