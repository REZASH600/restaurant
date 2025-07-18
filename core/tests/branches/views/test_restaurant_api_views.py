import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestRestaurantApiViews:
    def test_list_restaurants(self, admin_client, multiple_restaurants):
        url = reverse("branches:api_v1:restaurant_list")
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == len(multiple_restaurants)

    def test_list_restaurants_unauthenticated(self, api_client):
        url = reverse("branches:api_v1:restaurant_list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_restaurant_as_admin(self, admin_client):
        url = reverse("branches:api_v1:restaurant_create")
        data = {
            "name": "New Restaurant",
            "description": "Nice place",
            "address": "123 Street",
            "city": "CityX",
            "postal_code": "1234567890",
            "phone_number1": "09111222333",
            "phone_number2": "02122223333",
            "email": "new@example.com",
            "website": "http://newplace.com",
            "rate": 4.0,
            "latitude": 35.0,
            "longitude": 51.0,
            "support_of_range_delivery": True,
            "out_of_range_delivery_fee": 5.0,
            "max_out_of_range_distance": 10.0,
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]

    def test_create_restaurant_as_unauthenticated(self, api_client):
        url = reverse("branches:api_v1:restaurant_create")
        data = {
            "name": "New Restaurant",
            "description": "Nice place",
            "address": "123 Street",
            "city": "CityX",
            "postal_code": "1234567890",
            "phone_number1": "09111222333",
            "phone_number2": "02122223333",
            "email": "new@example.com",
            "website": "http://newplace.com",
            "rate": 4.0,
            "latitude": 35.0,
            "longitude": 51.0,
            "support_of_range_delivery": True,
            "out_of_range_delivery_fee": 5.0,
            "max_out_of_range_distance": 10.0,
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_restaurant_as_admin(self, admin_client, restaurant):
        url = reverse("branches:api_v1:restaurant_update", args=[restaurant.pk])
        data = {"description": "Updated description"}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["description"] == "Updated description"

    def test_patch_restaurant_as_unauthenticated(self, api_client, restaurant):
        url = reverse("branches:api_v1:restaurant_update", args=[restaurant.pk])
        data = {"description": "Should not update"}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_restaurant(self, api_client, restaurant):
        url = reverse("branches:api_v1:restaurant_detail", args=[restaurant.pk])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == restaurant.name
