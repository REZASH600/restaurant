from rest_framework import serializers
from apps.menus import models


class UserFavoriteMenuItemSerializer(serializers.ModelSerializer):
    # menu_item = serializers.HyperlinkedRelatedField(
    #     view_name="menuitem-detail", read_only=True, lookup_field="pk"
    # )

    class Meta:
        model = models.UserFavoriteMenuItems
        fields = ["id", "menu_item", "created_at"]
        read_only_fields = ["created_at"]
