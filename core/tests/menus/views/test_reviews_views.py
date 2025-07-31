import pytest
from django.urls import reverse
from rest_framework import status
from apps.menus import models

@pytest.mark.django_db
class TestReviewsViews:
    reveiws_detail_url = "menus:api_v1:reviews_admin_retrieve_update_delete"
    reveiws_list_url = "menus:api_v1:reviews_list"
    reveiws_create_url = "menus:api_v1:reviews_create"

    def test_get_review_as_admin(self, admin_client, review):
        url = reverse(self.reveiws_detail_url, args=[review.id])
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == review.id

    def test_patch_review_as_admin(self, admin_client, review):
        url = reverse(self.reveiws_detail_url, args=[review.id])
        data = {"rate": 4}
        response = admin_client.patch(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        review.refresh_from_db()
        assert review.rate == 4

    def test_delete_review_as_admin(self, admin_client, review):
        url = reverse(self.reveiws_detail_url, args=[review.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not models.Reviews.objects.filter(id=review.id).exists()

    def test_access_forbidden_for_normal_user(self, normal_user_client, review):
        url = reverse(self.reveiws_detail_url, args=[review.id])
        response = normal_user_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_reviews_published_only_for_normal_user(self, normal_user_client, review):
        review.is_published = True
        review.save()
        url = reverse(self.reveiws_list_url)
        response = normal_user_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        for item in response.data["results"]:
            assert item["is_published"] is True

    def test_list_all_reviews_for_staff(self, admin_client, review):
        review.is_published = False
        review.save()
        url = reverse(self.reveiws_list_url)
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert any(r["id"] == review.id for r in response.data["results"])

    def test_create_review_as_authorized(self, admin_client, menu_item_with_relations):
        url = reverse(self.reveiws_create_url)
        payload = {
            "menu_item": menu_item_with_relations.id,
            "restaurant": menu_item_with_relations.restaurant.all().first().id,
            "rate": 5,
            "comment": "Great food!",
            "is_published": True,
        }
        response = admin_client.post(url, data=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert models.Reviews.objects.filter(comment="Great food!").exists()

    def test_create_review_forbidden_for_unauthorized(self, api_client, menu_item_with_relations):
        url = reverse(self.reveiws_create_url)
        payload = {
            "menu_item": menu_item_with_relations.id,
            "restaurant": menu_item_with_relations.restaurant.all().first().id,
            "rate": 4,
            "comment": "Nice!",
            "is_published": True,
        }
        response = api_client.post(url, data=payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

