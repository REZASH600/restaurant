import pytest
from rest_framework import status
from django.urls import reverse
from apps.menus import models
from decimal import Decimal
import factory

@pytest.mark.django_db
class TestMenuItemViews:

    menuitem_list_url = "menus:api_v1:menuitem_list"
    menuitem_retrieve_url = "menus:api_v1:menuitem_retrieve"
    menuitem_create_url = "menus:api_v1:menuitem_create"
    menuitem_update_delete_url = "menus:api_v1:menuitem_update_delete"

    def test_list_menu_items(self, api_client, menu_item_with_relations):
        url = reverse(self.menuitem_list_url)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(
            item["id"] == menu_item_with_relations.id
            for item in response.data["results"]
        )

    def test_retrieve_menu_item(self, api_client, menu_item_with_relations):
        url = reverse(self.menuitem_retrieve_url, args=[menu_item_with_relations.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == menu_item_with_relations.id

    def test_create_menu_item_as_admin(
        self, admin_client, multiple_categories, multiple_restaurants
    ):
        url = reverse(self.menuitem_create_url)
        payload = {
            "name": "New Menu Item",
            "description": "Yummy",
            "price": 15.5,
            "category": multiple_categories[0].id,
            "restaurant": multiple_restaurants[0].id,
            "preparation_time": 10,
            "is_available": True,
        }
        response = admin_client.post(url, data=payload)
        assert response.status_code == status.HTTP_201_CREATED

        assert models.MenuItems.objects.filter(name="New Menu Item").exists()

    def test_create_menu_item_as_normal_user_forbidden(
        self, normal_user_client, multiple_categories, multiple_restaurants
    ):
        url = reverse(self.menuitem_create_url)
        payload = {
            "name": "Forbidden Item",
            "description": "Nope",
            "price": 12,
            "category": multiple_categories[0].id,
            "restaurant": multiple_restaurants[0].id,
            "preparation_time": 5,
            "is_available": True,
        }
        response = normal_user_client.post(url, data=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_menu_item_as_admin(self, admin_client, menu_item_with_relations):
        url = reverse(
            self.menuitem_update_delete_url, args=[menu_item_with_relations.id]
        )
        payload = {"price": 99.99}
        response = admin_client.patch(url, data=payload)
        assert response.status_code == status.HTTP_200_OK
        menu_item_with_relations.refresh_from_db()
        assert menu_item_with_relations.price == Decimal("99.99")

    def test_update_menu_item_as_normal_user_forbidden(
        self, normal_user_client, menu_item_with_relations
    ):
        url = reverse(
            self.menuitem_update_delete_url, args=[menu_item_with_relations.id]
        )
        payload = {"price": 99.99}
        response = normal_user_client.patch(url, data=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_menu_item_as_admin(self, admin_client, menu_item_with_relations):
        url = reverse(
            self.menuitem_update_delete_url, args=[menu_item_with_relations.id]
        )
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not models.MenuItems.objects.filter(
            id=menu_item_with_relations.id
        ).exists()

    def test_delete_menu_item_as_normal_user_forbidden(
        self, normal_user_client, menu_item_with_relations
    ):
        url = reverse(
            self.menuitem_update_delete_url, args=[menu_item_with_relations.id]
        )
        response = normal_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # --------- Filter tests ----------

    def test_filter_by_category(
        self, api_client, multiple_categories, menu_item_with_relations
    ):
        category = multiple_categories[0]
        url = reverse(self.menuitem_list_url)
        response = api_client.get(url, {"category": category.name})
        assert response.status_code == status.HTTP_200_OK
        assert any(
            item["id"] == menu_item_with_relations.id
            for item in response.data["results"]
        )

    def test_filter_by_price_range(self, api_client, menu_item_with_relations):
        low = menu_item_with_relations.price - 1
        high = menu_item_with_relations.price + 1
        url = reverse(self.menuitem_list_url)
        response = api_client.get(url, {"price_min": low, "price_max": high})
        assert response.status_code == status.HTTP_200_OK
        assert any(
            item["id"] == menu_item_with_relations.id
            for item in response.data["results"]
        )

    def test_filter_by_search(self, api_client, menu_item_with_relations):
        search_text = menu_item_with_relations.name

        url = reverse(self.menuitem_list_url)
        response = api_client.get(url, {"search": search_text})
        assert response.status_code == status.HTTP_200_OK
        assert any(
            search_text.lower() in item["name"].lower()
            for item in response.data["results"]
        )

    def test_filter_by_is_available(self, api_client, menu_item_with_relations):
        url = reverse(self.menuitem_list_url)
        response = api_client.get(url, {"is_available": True})
        assert response.status_code == status.HTTP_200_OK
        assert all(item["is_available"] for item in response.data["results"])


@pytest.mark.django_db
class TestMenuItemImageViews:
    image_create_url = "menus:api_v1:menuitem_images_create"
    image_delete_url = "menus:api_v1:menuitem_images_delete"

    def test_create_menu_item_image_as_admin(
        self, admin_client, menu_item_with_relations
    ):
        url = reverse(self.image_create_url)
        payload = {
            "menu_item": menu_item_with_relations.id,
            "image": factory.django.ImageField(color="blue"),
        }
        response = admin_client.post(url, data=payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_menu_item_image_as_normal_user_forbidden(
        self, normal_user_client, menu_item_with_relations
    ):
        url = reverse(self.image_create_url)
        payload = {"menu_item": menu_item_with_relations.id}
        response = normal_user_client.post(url, data=payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_menu_item_image_as_admin(self, admin_client, menu_item_image):
        url = reverse(self.image_delete_url, args=[menu_item_image.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not models.MenuItemImages.objects.filter(id=menu_item_image.id).exists()

    def test_delete_menu_item_image_as_normal_user_forbidden(
        self, normal_user_client, menu_item_image
    ):
        url = reverse(self.image_delete_url, args=[menu_item_image.id])
        response = normal_user_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
