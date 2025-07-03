from django.urls import path
from . import views

app_name = "api_v1"


urlpatterns = [
    path(
        "favorite-items/",
        views.UserFavoriteMenuItemListCreateView.as_view(),
        name="user-favorite-menuitem-list-create",
    ),
    path(
        "favorite-items/<int:pk>/",
        views.UserFavoriteMenuItemDestroyView.as_view(),
        name="favorite-menuitem-delete",
    ),
    path("",views.MenuItemListAPIView.as_view(),name="menuitem-list")
]
