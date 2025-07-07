from utils.permissions import IsAdminOrIsPersonnel


class IsSuperuserOrIsPersonelOrBuyer(IsAdminOrIsPersonnel):
    """
    Custom permission to allow access only to:
    - admin users (staff or superuser), or
    - authenticated users who have purchased the related menu item.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check parent permission first
        if super().has_permission(request, view):
            return True

        # and user buy this menu item
