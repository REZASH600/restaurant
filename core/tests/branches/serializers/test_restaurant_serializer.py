import pytest
from apps.branches.api.v1.serializers import (
    RestaurantListSerializer,
    RestaurantDetailSerializer
)


@pytest.mark.django_db
class TestRestaurantListSerializer:
    def test_fields_exist(self, restaurant):
        serializer = RestaurantListSerializer(instance=restaurant)
        data = serializer.data

        assert set(data.keys()) == {
            "name",
            "description",
            "phone_number1",
            "address",
            "city",
            "postal_code",
            "is_open_now",
        }

    def test_is_open_now_field(self, restaurant):
        serializer = RestaurantListSerializer(instance=restaurant)
        assert "is_open_now" in serializer.data


@pytest.mark.django_db
class TestRestaurantDetailSerializer:
    def test_all_expected_fields(self, restaurant):
        serializer = RestaurantDetailSerializer(instance=restaurant)
        data = serializer.data

        expected_fields = {
            "name", "description", "logo", "address", "city", "postal_code",
            "phone_number1", "phone_number2", "email", "website", "rate",
            "latitude", "longitude", "support_of_range_delivery",
            "out_of_range_delivery_fee", "max_out_of_range_distance",
            "is_open_now", "created_at", "updated_at"
        }

        assert set(data.keys()) == expected_fields
