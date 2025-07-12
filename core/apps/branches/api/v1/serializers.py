from rest_framework import serializers
from apps.branches import models


class RestaurantListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Restaurant
        fields = [
            "name",
            "description",
            "phone_number1",
            "address",
            "city",
            "postal_code",
            "is_open_now",
        ]


class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Restaurant
        fields = [
            "name",
            "description",
            "logo",
            "address",
            "city",
            "postal_code",
            "phone_number1",
            "phone_number2",
            "email",
            "website",
            "rate",
            "latitude",
            "longitude",
            "support_of_range_delivery",
            "out_of_range_delivery_fee",
            "max_out_of_range_distance",
            "is_open_now",
            "created_at",
            "updated_at",
        ]


class RestaurantOpeningHoursSerializer(serializers.ModelSerializer):

    restaurant_name = serializers.SerializerMethodField()

    class Meta:
        model = models.RestaurantOpeningHours
        fields = [
            "restaurant",
            "restaurant_name",
            "day",
            "open_time",
            "close_time",
            "is_closed",
        ]

    def get_restaurant_name(self, obj):
        return obj.restaurant.name
