from django.urls import path
from . import views

app_name = "api_v1"

urlpatterns = [
    path("", views.RestaurantListApiView.as_view(), name="restaurant_list"),
    path("create/", views.RestaurantCreateApiView.as_view(), name="restaurant_create"),
    path(
        "<int:pk>/", views.RestaurantRetrieveApiView.as_view(), name="restaurant_detail"
    ),
    path(
        "<int:pk>/update/",
        views.RestaurantUpdateApiView.as_view(),
        name="restaurant_update",
    ),
    path(
        "opening-hours/create/",
        views.RestaurantOpeningHoursCreateApiView.as_view(),
        name="opening_hours_create",
    ),
    path(
        "opening-hours/",
        views.RestaurantOpeningHoursListApiView.as_view(),
        name="opening_hours_list",
    ),
    path(
        "opening-hours/<int:pk>/update/",
        views.RestaurantOpeningHoursUpdateApiView.as_view(),
        name="opening_hours_update",
    ),
]
