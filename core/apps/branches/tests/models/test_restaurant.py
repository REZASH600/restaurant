# tests/test_restaurant_model.py

import pytest
from decimal import Decimal


@pytest.mark.django_db
class TestRestaurantModel:

    def test_str_method(self, restaurant):
        assert str(restaurant) == f"{restaurant.name}:{restaurant.description}"

    def test_rate_range(self, restaurant):
        assert Decimal("0.0") <= restaurant.rate <= Decimal("5.0")

    def test_latitude_and_longitude(self, restaurant):
        assert -90 <= restaurant.latitude <= 90
        assert -180 <= restaurant.longitude <= 180

    def test_get_cached_rate_returns_default_if_not_cached(self, restaurant):
        assert restaurant.get_cached_rate() == restaurant.rate

    def test_support_of_range_delivery_default_true(self, static_restaurant):
        assert static_restaurant.support_of_range_delivery is True

    def test_out_of_range_delivery_fee_positive(self, restaurant):
        assert restaurant.out_of_range_delivery_fee >= 0

    def test_max_out_of_range_distance_positive(self, restaurant):
        assert restaurant.max_out_of_range_distance >= 0

    def test_optional_fields_nullable(self, restaurant_without_optional):
        assert restaurant_without_optional.phone_number2 is None
        assert restaurant_without_optional.email is None

    def test_is_open_now_false_without_opening_hours(self, restaurant):
        assert restaurant.is_open_now is False

    def test_static_restaurant_values(self, static_restaurant):
        assert static_restaurant.name == "Test"
        assert static_restaurant.phone_number1 == "09121234568"
        assert static_restaurant.website == "http://example.com"
        assert static_restaurant.latitude == 30.0
        assert static_restaurant.longitude == 50.0
        assert static_restaurant.rate == 4.1
