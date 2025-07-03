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


class MenuItemListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    # menu_item = serializers.HyperlinkedRelatedField(
    #     view_name="menuitem-detail", read_only=True, lookup_field="pk"
    # )

    images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="image_file",
    )

    class Meta:
        model = models.MenuItems
        fields = [
            "id",
            "name",
            "description",
            "price",
            "is_available",
            "category",
            "images",
            "preparation_time",
            "rate"
        ]
