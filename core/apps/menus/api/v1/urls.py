from django.urls import path
from . import views

app_name = "api_v1"


urlpatterns = [
    path(
        "favorite-items/",
        views.UserFavoriteMenuItemListCreateApiView.as_view(),
        name="user_favorite_menuitem_list_create",
    ),
    path(
        "favorite-items/<int:pk>/",
        views.UserFavoriteMenuItemDestroyApiView.as_view(),
        name="favorite_menuitem_delete",
    ),
    path("", views.MenuItemListApiView.as_view(), name="menuitem_list"),
    path(
        "<int:pk>/",
        views.MenuItemRetrieveUpdateDeleteApiView.as_view(),
        name="menuitem_retrieve_update_delete",
    ),
    path("create/", views.MenuItemCreateApiView.as_view(), name="menuitem_create"),
    path("create/images/",views.MenuItemImagesCreateApiView.as_view(),name="menuitem_images_create"
    )
]
