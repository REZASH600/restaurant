from rest_framework import (
    generics,
    permissions as drf_permissions,
    filters,
    mixins,
    views,
    status,
    response,
)
from django.contrib.auth import update_session_auth_hash

from django_filters.rest_framework import DjangoFilterBackend
from apps.accounts import models
from . import serializers, permissions
import random
from django.core.cache import cache
from apps.accounts.tasks import send_email,send_sms


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
            return response.Response(
                {"message": "Password updated successfully."}, status=status.HTTP_200_OK
            )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailApiView(views.APIView):
    permission_classes = [drf_permissions.IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        temp_email = profile.temporary_email

        if not temp_email:
            return response.Response(
                {"error": "No temporary email found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = random.randint(100000, 999999)
        cache.set(f"verify_email:{request.user.id}", token, timeout=300)  # 5 minutes

        send_email.send_verification_email.delay(temp_email, token)
        return response.Response(
            {"message": f"Verification token sent to {temp_email}"},
            status=status.HTTP_200_OK,
        )


class VerifyEmailApiView(views.APIView):
    serializer_class = serializers.VerifyTokenApiSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        cached_token = cache.get(f"verify_email:{request.user.id}")

        if not cached_token:
            return response.Response(
                {"error": "Token expired or not found."}, status=400
            )

        if token != str(cached_token):
            return response.Response({"error": "Invalid token."}, status=400)

        profile = request.user.profile
        if profile.temporary_email:
            request.user.email = profile.temporary_email
            request.user.save()
            profile.temp_email = None
            profile.save()
            cache.delete(f"verify_email:{request.user.id}")
            return response.Response(
                {"message": "Email verified and updated."}, status=200
            )

        return response.Response({"error": "No temporary email found."}, status=400)




class SendPhoneOtpApiView(views.APIView):
    permission_classes = [drf_permissions.IsAuthenticated]

    def post(self, request):
        phone = request.user.phone
        if request.user.is_phone_verified:
            return response.Response(
                {"error": "Phone number is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = random.randint(100000, 999999)
        cache.set(f"verify_phone:{request.user.id}", token, timeout=300)  # 5 minutes

        send_sms.send_verification_sms.delay(phone, token)

        return response.Response(
            {"message": f"Verification code sent to {phone}"},
            status=status.HTTP_200_OK,
        )


class VerifyPhoneOtpApiView(views.APIView):
    serializer_class = serializers.VerifyTokenApiSerializer
    permission_classes = [drf_permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        cached_token = cache.get(f"verify_phone:{request.user.id}")

        if not cached_token:
            return response.Response(
                {"error": "Token expired or not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if token != str(cached_token):
            return response.Response(
                {"error": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cache.delete(f"verify_phone:{request.user.id}")

        request.user.is_phone_verified = True
        request.user.save()

        return response.Response(
            {"message": "Phone number verified successfully."},
            status=status.HTTP_200_OK,
        )
