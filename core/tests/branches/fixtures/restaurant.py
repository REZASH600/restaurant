import pytest
from tests.branches.factories import RestaurantFactory





@pytest.fixture
def restaurant_without_optional():
    return RestaurantFactory(without_optional_fields=True)




