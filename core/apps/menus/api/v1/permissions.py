from rest_framework import permissions

class IsAdminOrMenuItemBuyer(permissions.BasePermission):

    """
    Custom permission to allow access only to:
    - admin users (staff or superuser), or
    - authenticated users who have purchased the related menu item.
    """


    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not user.is_authenticated:
            return False
    
        if user.is_staff or user.is_superuser:
            return True


    
        # and user buy this menu item
