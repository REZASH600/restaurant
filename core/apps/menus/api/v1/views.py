from rest_framework import generics, permissions as drf_permissions
from apps.menus import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filterset import MenuItemFilter, ReviewFilter


class UserFavoriteMenuItemListCreateApiView(generics.ListCreateAPIView):
    serializer_class = serializers.UserFavoriteMenuItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        return models.UserFavoriteMenuItems.objects.filter(
            user_profile=self.request.user.profile
        )

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class UserFavoriteMenuItemDestroyApiView(generics.DestroyAPIView):
    serializer_class = serializers.UserFavoriteMenuItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        return models.UserFavoriteMenuItems.objects.filter(
            user_profile=self.request.user.profile
        )


class MenuItemListApiView(generics.ListAPIView):
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemListSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemFilter


class MenuItemRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "get", "delete"]
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemDetailSerializer


class MenuItemCreateApiView(generics.CreateAPIView):
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemDetailSerializer
    permission_classes = [
        drf_permissions.IsAdminUser,
    ]


class MenuItemImagesCreateApiView(generics.CreateAPIView):
    queryset = models.MenuItemImages.objects.all()
    serializer_class = serializers.MenuItemImageSerializer
    permission_classes = [
        drf_permissions.IsAdminUser,
    ]


class MenuItemImagesDestroyApiView(generics.DestroyAPIView):
    queryset = models.MenuItemImages.objects.all()
    permission_classes = [
        drf_permissions.IsAdminUser,
    ]


class ReviewsAdminRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "get", "delete"]
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.ReviewsAdminSerializer
    permission_classes = [
        drf_permissions.IsAdminUser,
    ]


class ReviewsListAPIView(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_queryset(self):
        qs = models.Reviews.objects.all()
        if not self.request.user.is_staff:
            qs = qs.filter(is_published=True)
        return qs
