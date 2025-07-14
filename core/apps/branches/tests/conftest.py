import pytest
from apps.branches.tests.factories import (
    RestaurantFactory,
    RestaurantOpeningHoursFactory,
)
from datetime import time





@pytest.fixture
def restaurant_without_optional():
    return RestaurantFactory(without_optional_fields=True)


@pytest.fixture
def static_restaurant():
    return RestaurantFactory(static_test_values=True)


@pytest.fixture
def opening_hour_default(restaurant):
    return RestaurantOpeningHoursFactory(restaurant=restaurant)

@pytest.fixture
def opening_hour_tuesday_open(restaurant):
    return RestaurantOpeningHoursFactory(restaurant=restaurant, tuesday_open=True)

@pytest.fixture
def opening_hour_wednesday_closed(restaurant):
    return RestaurantOpeningHoursFactory(restaurant=restaurant, wednesday_closed=True)

@pytest.fixture
def opening_hour_sunday_midnight(restaurant):
    return RestaurantOpeningHoursFactory(restaurant=restaurant, sunday_midnight=True)

@pytest.fixture
def opening_hour_saturday_noon(restaurant):
    return RestaurantOpeningHoursFactory(restaurant=restaurant, saturday_noon=True)


@pytest.fixture
def closed_hours(restaurant):
    return RestaurantOpeningHoursFactory(restaurant=restaurant, closed=True)

@pytest.fixture
def all_days_open_hours(restaurant):
    return [
        RestaurantOpeningHoursFactory(restaurant=restaurant, day=day, is_closed=False, open_time=time(9, 0), close_time=time(17, 0))
        for day in range(7)
    ]
