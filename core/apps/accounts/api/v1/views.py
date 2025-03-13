from rest_framework import generics, permissions as drf_permissions, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts import models
from . import serializers, permissions


class UserListApiView(generics.ListAPIView):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (drf_permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ("is_active", "is_superuser", "is_staff", "is_phone_verified")
    search_fields = (
        "phone",
        "username",
        "email",
    )


class ProfileApiView(generics.RetrieveUpdateAPIView):
    http_method_names = ["get", "patch"]
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsOwnerOrAdminUser,)
