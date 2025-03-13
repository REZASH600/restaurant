from rest_framework import generics, permissions, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts import models
from . import serializers


class UserList(generics.ListAPIView):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ("is_active", "is_superuser", "is_staff", "is_phone_verified")
    search_fields = ("phone","username","email",)
