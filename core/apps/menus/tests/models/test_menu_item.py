import pytest

from django.core.cache import cache


@pytest.mark.django_db
class TestMenuItemsModel:

    def test_str_method(self, menu_item_with_relations):
        string_repr = str(menu_item_with_relations)
        assert menu_item_with_relations.name in string_repr
        assert str(menu_item_with_relations.price) in string_repr

    def test_fields(self, menu_item_with_relations):
        assert menu_item_with_relations.price > 0
        assert isinstance(menu_item_with_relations.is_available, bool)
        assert menu_item_with_relations.preparation_time >= 0
        assert 0 <= menu_item_with_relations.rate <= 5
        assert menu_item_with_relations.stock_quantity >= 0

    def test_many_to_many_relations(
        self, menu_item_with_relations, multiple_categories, multiple_restaurants
    ):
        assert menu_item_with_relations.category.count() == len(multiple_categories)
        assert menu_item_with_relations.restaurant.count() == len(multiple_restaurants)

    def test_get_cached_rate_returns_cached_value(self, menu_item_with_relations):
        key = f"menu_item_rating_{menu_item_with_relations.id}"
        cache.set(key, {"avg": 4.75})

        cached_rate = menu_item_with_relations.get_cached_rate()
        assert cached_rate == 4.75

    def test_get_cached_rate_returns_default_rate_when_cache_empty(
        self, menu_item_with_relations
    ):
        key = f"menu_item_rating_{menu_item_with_relations.id}"
        cache.delete(key)

        cached_rate = menu_item_with_relations.get_cached_rate()
        assert cached_rate == round(menu_item_with_relations.rate, 2)
