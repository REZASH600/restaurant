import pytest
from apps.branches.api.v1.serializers import RestaurantOpeningHoursSerializer


@pytest.mark.django_db
class TestRestaurantOpeningHoursSerializer:
    def test_fields_and_restaurant_name(self, opening_hour_default):
        serializer = RestaurantOpeningHoursSerializer(instance=opening_hour_default)
        data = serializer.data

        assert set(data.keys()) == {
            "restaurant",
            "restaurant_name",
            "day",
            "open_time",
            "close_time",
            "is_closed"
        }

        assert data["restaurant_name"] == opening_hour_default.restaurant.name
