import pytest
from tests.menus.factories import CategoryFactory


@pytest.fixture
def category_with_restaurants(multiple_restaurants):
    return CategoryFactory(restaurant=multiple_restaurants)


@pytest.fixture
def multiple_categories(multiple_restaurants):
    return CategoryFactory.create_batch(2, restaurant=multiple_restaurants)