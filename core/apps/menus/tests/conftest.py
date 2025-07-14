import pytest
from .factories import (
    CategoryFactory,
    MenuItemsFactory,
    MenuItemImagesFactory,
    ReviewsFactory,
)


@pytest.fixture
def category_with_restaurants(multiple_restaurants):
    return CategoryFactory(restaurant=multiple_restaurants)


@pytest.fixture
def multiple_categories(multiple_restaurants):
    return CategoryFactory.create_batch(2, restaurant=multiple_restaurants)


@pytest.fixture
def menu_item_with_relations(multiple_categories, multiple_restaurants):
    return MenuItemsFactory(
        category=multiple_categories, restaurant=multiple_restaurants
    )


@pytest.fixture
def menu_item_image():
    return MenuItemImagesFactory()


@pytest.fixture
def review(fake_profile, menu_item_with_relations):
    return ReviewsFactory(
        user_profile=fake_profile,
        menu_item=menu_item_with_relations,
        restaurant=menu_item_with_relations.restaurant.first(),
    )
