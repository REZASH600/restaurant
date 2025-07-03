from rest_framework import generics, permissions as drf_permissions
from apps.menus import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filterset import MenuItemFilter


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




class MenuItemListAPIView(generics.ListAPIView):
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemListSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemFilter