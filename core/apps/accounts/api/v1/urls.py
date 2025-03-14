from django.urls import path
from . import views

app_name = "api_v1"

urlpatterns = [
    path("list/", views.UserListApiView.as_view(), name="user_list"),
    path("profile/<int:pk>/", views.ProfileApiView.as_view(), name="user_profile"),
    path("register/", views.RegisterUserApiView.as_view(), name="user_register"),
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change_password",
    ),
]
