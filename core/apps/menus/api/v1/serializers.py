from rest_framework import serializers
from apps.menus import models
from django.urls import reverse


class UserFavoriteMenuItemSerializer(serializers.ModelSerializer):
    menu_item_link = serializers.HyperlinkedRelatedField(
        view_name="menus:api_v1:menuitem_retrieve",
        read_only=True,
        source="menu_item",
        lookup_field="pk",
    )

    class Meta:
        model = models.UserFavoriteMenuItems
        fields = ["id", "menu_item", "created_at", "menu_item_link"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user_profile"] = user.profile
        return super().create(validated_data)


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


class ReviewsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user_profile_data = serializers.SerializerMethodField()

    class Meta:
        model = models.Reviews
        fields = [
            "id",
            "menu_item",
            "comment",
            "rate",
            "restaurant",
            "is_published",
            "user_profile_data",
            "created_at",
            "updated_at",
        ]

    def get_user_profile_data(self, obj):
        profile = obj.user_profile
        request = self.context.get("request")

        return {
            "id": profile.id,
            "username": profile.user.username,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "profile_picture": request.build_absolute_uri(profile.profile_picture.url),
        }

    def create(self, validated_data):
        """
        Create a new Review instance with the provided data.
        Automatically publish the review if the user is not admin/staff.
        """
        user = self.context.get("request").user

        # Only auto-publish if the user is NOT staff AND NOT superuser
        if not (user.is_staff or user.is_superuser):
            validated_data["is_published"] = True

        validated_data["user_profile"] = user.profile

        return models.Reviews.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):

    menu_item_list_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = [
            "id",
            "name",
            "description",
            "image_file",
            "restaurant",
            "menu_item_list_url",
            "created_at",
            "updated_at",
        ]

    def get_menu_item_list_url(self, obj):
        base_url = reverse("menus:api_v1:menuitem_list")
        return f"{base_url}?category_id={obj.id}"
