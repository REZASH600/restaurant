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
    path("verify-email/send/", views.SendEmailApiView.as_view(), name="send_email"),
    path("verify-email/check/", views.VerifyEmailApiView.as_view(), name="verify_email"),
    path("verify-phone/send/", views.SendPhoneOtpApiView.as_view(), name="send_phone_otp"),
    path("verify-phone/check/", views.VerifyPhoneOtpApiView.as_view(), name="verify_phone_otp"),
]
