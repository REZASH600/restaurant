from rest_framework import generics, permissions as drf_permissions
from apps.menus import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filterset import MenuItemFilter, ReviewFilter, CategoryFilter
from . import permissions
from utils.permissions import IsAdminOrIsPersonnel

class UserFavoriteMenuItemListCreateApiView(generics.ListCreateAPIView):
    serializer_class = serializers.UserFavoriteMenuItemSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def get_queryset(self):
        return models.UserFavoriteMenuItems.objects.filter(
            user_profile=self.request.user.profile
        )



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


    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at'] 


class MenuItemRetrieveApiView(generics.RetrieveAPIView):
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemDetailSerializer

class MenuItemUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "delete"]
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemDetailSerializer
    permission_classes = [
        IsAdminOrIsPersonnel,
    ]



class MenuItemCreateApiView(generics.CreateAPIView):
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.MenuItemDetailSerializer
    permission_classes = [
        IsAdminOrIsPersonnel,
    ]


class MenuItemImagesCreateApiView(generics.CreateAPIView):
    queryset = models.MenuItemImages.objects.all()
    serializer_class = serializers.MenuItemImageSerializer
    permission_classes = [
        IsAdminOrIsPersonnel,
    ]


class MenuItemImagesDestroyApiView(generics.DestroyAPIView):
    queryset = models.MenuItemImages.objects.all()
    permission_classes = [
       IsAdminOrIsPersonnel,
    ]


class ReviewsAdminRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "get", "delete"]
    queryset = models.MenuItems.objects.all()
    serializer_class = serializers.ReviewsAdminSerializer
    permission_classes = [
        IsAdminOrIsPersonnel,
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
        user = self.request.user
        if not (user.is_staff or user.is_superuser) :
            qs = qs.filter(is_published=True)
        return qs


class ReviewsCreateApiView(generics.CreateAPIView):
    queryset = models.Reviews.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [
        permissions.IsAdminOrIsPersonelOrBuyer,
    ]



class CategoryAdminRetrieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["patch", "get", "delete"]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [
        IsAdminOrIsPersonnel,
    ]


class CategoryListApiView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at'] 
   



    



