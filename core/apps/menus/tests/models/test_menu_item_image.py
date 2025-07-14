import pytest


@pytest.mark.django_db
class TestMenuItemImagesModel:

    def test_image_file_exists(self, menu_item_image):
        assert menu_item_image.image_file is not None
        assert "menu_items/" in str(menu_item_image.image_file)

    def test_menu_item_relation(self, menu_item_image):
        assert menu_item_image.menu_item is not None
        assert menu_item_image.menu_item.__class__.__name__ == "MenuItems"

    def test_str_method(self, menu_item_image):
        assert str(menu_item_image) != ""