from django.urls import path, include


app_name = "branches"
urlpatterns = [path("api/v1/", include("apps.branches.api.v1.urls"))]
