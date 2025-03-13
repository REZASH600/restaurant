from rest_framework import serializers
from apps.accounts import models


class UserListSerializer(serializers.ModelSerializer):
    # profile = serializers.HyperlinkedRelatedField(
    #     read_only=True, view_name="profile_user"
    # )

    class Meta:
        model = models.MyUser
        fields = "__all__"
