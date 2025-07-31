import pytest
from django.urls import reverse
from rest_framework import status
from apps.menus import models

@pytest.mark.django_db
class TestCategoryViews:
    category_detail_url = "menus:api_v1:category_admin_retrieve_update_delete"
    category_list_url = "menus:api_v1:category_list"

    def test_get_category_as_admin(self, admin_client, category_with_restaurants):
        url = reverse(self.category_detail_url, args=[category_with_restaurants.id])
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == category_with_restaurants.id

    def test_patch_category_as_admin(self, admin_client, category_with_restaurants):
        url = reverse(self.category_detail_url, args=[category_with_restaurants.id])
        data = {"name": "Updated Category"}
        response = admin_client.patch(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        category_with_restaurants.refresh_from_db()
        assert category_with_restaurants.name == "Updated Category"

    def test_delete_category_as_admin(self, admin_client, category_with_restaurants):
        url = reverse(self.category_detail_url, args=[category_with_restaurants.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not models.Category.objects.filter(id=category_with_restaurants.id).exists()

    def test_access_forbidden_for_normal_user(self, normal_user_client, category_with_restaurants):
        url = reverse(self.category_detail_url, args=[category_with_restaurants.id])
        response = normal_user_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_categories(self, api_client, category_with_restaurants):
        url = reverse(self.category_list_url)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(cat["id"] == category_with_restaurants.id for cat in response.data["results"])

    def test_filter_by_search(self, api_client, category_with_restaurants):
        url = reverse(self.category_list_url)
        response = api_client.get(url, {"search": category_with_restaurants.name})
        assert response.status_code == status.HTTP_200_OK
        assert any(category_with_restaurants.name in cat["name"] for cat in response.data["results"])
