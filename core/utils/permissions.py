from rest_framework import permissions


class IsAdminOrIsPersonnel(permissions.BasePermission):
    """
    Allows access to admin users (is_staff or is_superuser).
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_staff or user.is_superuser)