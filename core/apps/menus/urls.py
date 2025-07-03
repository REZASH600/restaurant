from django.urls import path,include


app_name = "menus"

urlpatterns = [
    path("api/v1/", include("apps.menus.api.v1.urls"))
]