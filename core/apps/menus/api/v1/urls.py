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
    path(
        "images/create/",
        views.MenuItemImagesCreateApiView.as_view(),
        name="menuitem_images_create",
    ),
    path(
        "images/delete/<int:pk>/",
        views.MenuItemImagesDestroyApiView.as_view(),
        name="menuitem_images_delete",
    ),
    path(
        "reviews/admin/<int:pk>/",
        views.ReviewsAdminRetrieveUpdateDeleteApiView.as_view(),
        name="reviews_admin_retrieve_update_delete",
    ),
    path("reviews/", views.ReviewsListAPIView.as_view(), name="reviews_list"),
    path(
        "reveiws/create/", views.ReviewsCreateApiView.as_view(), name="reviews_create"
    ),
    path(
        "category/admin/<int:pk>/",
        views.CategoryAdminRetrieveUpdateDeleteApiView.as_view(),
        name="category_admin_retrieve_update_delete",
    ),
    path("category/list/", views.CategoryListApiView.as_view(), name="category_list"),
]
