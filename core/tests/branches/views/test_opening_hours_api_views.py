import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRestaurantOpeningHoursViews:

    def test_admin_can_create_opening_hours(self, admin_client, restaurant):
        url = reverse("branches:api_v1:opening_hours_create")
        data = {
            "restaurant": restaurant.id,
            "day": 2,  # Wednesday
            "open_time": "10:00:00",
            "close_time": "22:00:00",
            "is_closed": False,
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["day"] == 2
        assert response.data["is_closed"] is False

    def test_unauthenticated_user_cannot_create_opening_hours(
        self, api_client, restaurant
    ):
        url = reverse("branches:api_v1:opening_hours_create")
        data = {
            "restaurant": restaurant.id,
            "day": 0,
            "open_time": "08:00:00",
            "close_time": "17:00:00",
            "is_closed": False,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_can_list_all_opening_hours(self, admin_client, all_days_open_hours):
        url = reverse("branches:api_v1:opening_hours_list")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 7  # All days of week

    def test_admin_can_filter_opening_hours_by_day(
        self, admin_client, all_days_open_hours
    ):
        url = reverse("branches:api_v1:opening_hours_list")
        response = admin_client.get(url, data={"day": 1})  # Tuesday
        assert response.status_code == status.HTTP_200_OK
        for item in response.data["results"]:
            assert item["day"] == 1

    def test_admin_can_update_opening_hours(
        self, admin_client, opening_hour_saturday_noon
    ):
        url = reverse(
            "branches:api_v1:opening_hours_update", args=[opening_hour_saturday_noon.id]
        )
        data = {"is_closed": True}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["is_closed"] is True

    def test_unauthenticated_user_cannot_update_opening_hours(
        self, api_client, opening_hour_saturday_noon
    ):
        url = reverse(
            "branches:api_v1:opening_hours_update", args=[opening_hour_saturday_noon.id]
        )
        response = api_client.patch(url, {"is_closed": True})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
