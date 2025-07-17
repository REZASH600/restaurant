import pytest
from unittest.mock import patch
from tests.menus.factories import ReviewsFactory

@pytest.mark.django_db
class TestReviewsModel:

    def test_review_fields_and_relations(self, review):
        assert review.comment
        assert 0 <= review.rate <= 5
        assert review.user_profile is not None
        assert review.menu_item is not None
        assert review.restaurant is not None
        assert review.created_at is not None
        assert review.updated_at is not None
        assert isinstance(review.is_published, bool)

    def test_str_method(self, review):
        result = str(review)
        assert review.comment in result
        assert str(review.menu_item) in result
        assert str(review.user_profile) in result

    @patch("apps.menus.signals.update_menu_item_cache")
    @patch("apps.menus.signals.update_restaurant_cache")
    def test_post_save_signal_triggers_cache_updates(self, mock_restaurant_cache, mock_menu_cache, fake_profile, menu_item_with_relations):
        review = ReviewsFactory(
            user_profile=fake_profile,
            menu_item=menu_item_with_relations,
            restaurant=menu_item_with_relations.restaurant.first(),
            rate=4.0,
        )
        
        mock_menu_cache.assert_called_once_with(menu_item_with_relations.id, 4.0)
        mock_restaurant_cache.assert_called_once_with(menu_item_with_relations.restaurant.first().id, 4.0)

    @patch("apps.menus.signals.update_menu_item_cache")
    @patch("apps.menus.signals.update_restaurant_cache")
    def test_post_delete_signal_triggers_cache_updates(self, mock_restaurant_cache, mock_menu_cache, review):
        rid = review.restaurant.id
        mid = review.menu_item.id
        rate = float(review.rate)

        review.delete()

        mock_menu_cache.assert_called_once_with(mid, -rate)
        mock_restaurant_cache.assert_called_once_with(rid, -rate)