from django.urls import path
from . import views

app_name = "api_v1"


urlpatterns = [
    path(
        "favorite-menu-items/",
        views.UserFavoriteMenuItemListCreateView.as_view(),
        name="user-favorite-menuitem-list-create",
    ),
    path(
        "favorite-menu-items/<int:pk>/",
        views.UserFavoriteMenuItemDestroyView.as_view(),
        name="favorite-menuitem-delete",
    ),
]
