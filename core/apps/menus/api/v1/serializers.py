from rest_framework import serializers
from apps.menus import models


class UserFavoriteMenuItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.HyperlinkedRelatedField(
        view_name="menus:api_v1:menuitem_retrieve_update_delete", read_only=True, lookup_field="pk"
    )

    class Meta:
        model = models.UserFavoriteMenuItems
        fields = ["id", "menu_item", "created_at"]
        read_only_fields = ["created_at"]


class MenuItemImageSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=models.MenuItems.objects.all()
    )

    class Meta:
        model = models.MenuItemImages
        fields = ["id", "image_file", "menu_item"]


class MenuItemListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )



    images = MenuItemImageSerializer(read_only=True, many=True)

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
            "rate",

        ]



class CategorySlugOrPKRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Custom field that reads category by slug (name) but writes using pk.
    """

    def to_representation(self, obj):
        return obj.name

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class MenuItemDetailSerializer(serializers.ModelSerializer):
    category = CategorySlugOrPKRelatedField(
        queryset=models.Category.objects.all(), many=True
    )
    images = MenuItemImageSerializer(read_only=True, many=True)

    current_rate = serializers.SerializerMethodField()

    class Meta:
        model = models.MenuItems
        fields = [
            "id",
            "name",
            "description",
            "price",
            "is_available",
            "preparation_time",
            "rate",
            "current_rate",
            "stock_quantity",
            "category",
            "images",
            "created_at",
            "updated_at",
        ]

    def get_current_rate(self, obj):

        return obj.get_cached_rate()
