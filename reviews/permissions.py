from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Доступ на добавление, изменение и удаление только для администраторов.
    Просмотр доступен всем.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Доступ на изменение только для владельца объекта, удаление только для администратора.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return request.user and (request.user.is_staff or request.user == obj.user_id)
        return request.user == obj.user_id


class IsAuthenticatedToCreate(BasePermission):
    """
    Создавать данные может только аутентифицированный пользователь.
    Просмотр доступен всем.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
