from rest_framework import permissions


class IsOwnerOrAdminUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return request.user == obj.user



class AnonusUser(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return not request.user.is_authenticated
