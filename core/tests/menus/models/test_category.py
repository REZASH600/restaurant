import pytest


@pytest.mark.django_db
class TestCategoryModel:

    def test_str_method(self, category_with_restaurants):
        assert (
            str(category_with_restaurants)
            == category_with_restaurants.name
        )

    def test_category_fields(self, category_with_restaurants):
        assert category_with_restaurants.name is not None
        assert category_with_restaurants.description is not None
        assert category_with_restaurants.created_at is not None
        assert category_with_restaurants.updated_at is not None
        assert category_with_restaurants.restaurant.count() == 3

    def test_category_restaurant_relationship(
        self, category_with_restaurants, multiple_restaurants
    ):
        for rest in multiple_restaurants:
            assert rest in category_with_restaurants.restaurant.all()
