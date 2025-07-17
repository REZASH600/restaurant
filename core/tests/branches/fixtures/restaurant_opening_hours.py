
import pytest
from tests.branches.factories import RestaurantOpeningHoursFactory



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

