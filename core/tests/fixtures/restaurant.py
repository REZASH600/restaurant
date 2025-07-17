import pytest
from tests.branches.factories import RestaurantFactory, RestaurantOpeningHoursFactory
from datetime import time


@pytest.fixture
def restaurant():
    return RestaurantFactory()


@pytest.fixture
def multiple_restaurants():
    return RestaurantFactory.create_batch(3)


@pytest.fixture
def static_restaurant():
    return RestaurantFactory(static_test_values=True)


@pytest.fixture
def all_days_open_hours(restaurant):
    return [
        RestaurantOpeningHoursFactory(
            restaurant=restaurant,
            day=day,
            is_closed=False,
            open_time=time(9, 0),
            close_time=time(17, 0),
        )
        for day in range(7)
    ]
