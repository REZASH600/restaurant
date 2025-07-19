import pytest
from apps.menus.api.v1.serializers import CategorySerializer
from django.urls import reverse


@pytest.mark.django_db
class TestCategorySerializer:

    def test_category_serializer_output(self, category_with_restaurants, rf):
        request = rf.get("/")
        context = {"request": request}

        serializer = CategorySerializer(category_with_restaurants, context=context)
        data = serializer.data

        assert data["id"] == category_with_restaurants.id
        assert data["name"] == category_with_restaurants.name
        assert "menu_item_list_url" in data

        expected_url = f"{reverse('menus:api_v1:menuitem_list')}?category_id={category_with_restaurants.id}"
        assert data["menu_item_list_url"] == expected_url
