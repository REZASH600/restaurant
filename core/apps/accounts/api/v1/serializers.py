from rest_framework import serializers
from apps.accounts import models
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse


class UserListSerializer(serializers.ModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="accounts:api_v1:user_profile"
    )

    class Meta:
        model = models.MyUser
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):

    is_email_verified = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = [
            "first_name",
            "last_name",
            "profile_picture",
            "orders_count",
            "reviews_count",
            "temporary_email",
            "is_email_verified",
            "created_at",
            "updated_at",
        ]

    read_only_fields = ["order_count", "reviews_count"]

    def get_is_email_verified(self, obj):
        user = obj.user
        email = user.email
        temporary_email = obj.temporary_email
        if email and temporary_email and email == temporary_email:
            return True

        return False


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    class Meta:
        model = models.MyUser
        fields = ["username", "phone", "password1", "password2"]

    def validate_password1(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):

        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password1")
        validated_data["password"] = validated_data.pop("password2")
        user = models.MyUser.objects.create_user(**validated_data)
        return user


class ChangePassowrdSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def validate_old_password(self, value):
        user = self.context.get("request").user

        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "The old password is incorrect."}
            )

        return value

    def validate_password1(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):

        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        return attrs

    def save(self, **kwargs):
        """Update user's password."""
        user = self.context.get("request").user
        user.set_password(self.validated_data["password1"])
        user.save()
        return user


class VerifyTokenApiSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6)


class CheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Checkout
        fields = [
            "id",
            "address",
            "city",
            "state",
            "postal_code",
            "recipient_phone",
            "recipient_name",
            "is_default",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user_profile"] = request.user.profile
        return super().create(validated_data)

