from django.urls import path
from . import views

app_name = "api_v1"

urlpatterns = [
    path("user/list/", views.UserList.as_view(), name="user_list")]
