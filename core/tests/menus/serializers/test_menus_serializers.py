
import pytest
from apps.menus.api.v1.serializers import (
    MenuItemImageSerializer,
    MenuItemListSerializer,
    MenuItemDetailSerializer,
)





@pytest.mark.django_db
class TestMenuItemImageSerializer:

    def test_serialize_menu_item_image(self, menu_item_image, rf):
        request = rf.get("/")
        context = {"request": request}

        serializer = MenuItemImageSerializer(menu_item_image, context=context)
        data = serializer.data

        assert data["id"] == menu_item_image.id
        assert data["image_file"]

    def test_create_menu_item_image(self, menu_item_image):
        data = {
            "image_file": menu_item_image.image_file,
            "menu_item": menu_item_image.menu_item.id,
        }

        serializer = MenuItemImageSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        instance = serializer.save()

        assert instance.menu_item == menu_item_image.menu_item
        assert instance.image_file.name.endswith(".jpg")

@pytest.mark.django_db
class TestMenuItemSerializers:

    def test_menu_item_list_output(self, menu_item_with_relations, rf):
        request = rf.get("/")
        context = {"request": request}

        serializer = MenuItemListSerializer(menu_item_with_relations, context=context)
        data = serializer.data

        assert data["id"] == menu_item_with_relations.id
        assert data["name"] == menu_item_with_relations.name
        assert isinstance(data["category"], list)
        assert isinstance(data["images"], list)
        assert "description" in data
        assert "preparation_time" in data

    def test_menu_item_detail_output(self, menu_item_with_relations, rf):
        request = rf.get("/")
        context = {"request": request}

        serializer = MenuItemDetailSerializer(menu_item_with_relations, context=context)
        data = serializer.data

        assert data["id"] == menu_item_with_relations.id
        assert data["name"] == menu_item_with_relations.name
        assert "rate" in data
        assert "current_rate" in data
        assert "stock_quantity" in data
        assert isinstance(data["category"], list)
        assert isinstance(data["images"], list)