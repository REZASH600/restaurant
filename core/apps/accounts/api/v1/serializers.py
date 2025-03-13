from rest_framework import serializers
from apps.accounts import models


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



