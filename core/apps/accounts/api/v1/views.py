from rest_framework import (
    generics,
    permissions as drf_permissions,
    filters,
    mixins,
    views,
    status,
    response
)
from django.contrib.auth import update_session_auth_hash

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


class RegisterUserApiView(generics.CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (permissions.AnonusUser,)


class ChangePasswordApiView(views.APIView):
    serializer_class = serializers.ChangePassowrdSerializer
    permission_classes = (drf_permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            update_session_auth_hash(request, user)
            return response.Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
