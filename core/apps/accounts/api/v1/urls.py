from django.urls import path
from . import views

app_name = "api_v1"

urlpatterns = [
    path("user/list/", views.UserListApiView.as_view(), name="user_list"),
    path("user/profile/<int:pk>/",views.ProfileApiView.as_view(),name="user_profile")
    ]
