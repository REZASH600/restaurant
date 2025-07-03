from rest_framework import generics, permissions as drf_permissions
from apps.menus import models
from . import serializers


class UserFavoriteMenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.UserFavoriteMenuItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]


    def get_queryset(self):
        return models.UserFavoriteMenuItems.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)



class UserFavoriteMenuItemDestroyView(generics.DestroyAPIView):
    serializer_class = serializers.UserFavoriteMenuItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        return models.UserFavoriteMenuItems.objects.filter(user_profile=self.request.user.profile)