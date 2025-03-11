from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "phone", "username", "is_active", "is_staff", "is_superuser"]
    list_filter = ["is_active", "is_superuser", "is_staff"]
    search_fields = ["phone", "username", "email"]
    list_editable = ["is_active", "is_superuser", "is_staff"]
    ordering = ("phone",)
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("phone", "username", "email", "password"),
            },
        ),
        (
            "Personal Information",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_phone_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            "Group Permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_phone_verified",
                ),
            },
        ),
    )


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "reviews_count", "orders_count"]
    search_fields = [
        "user.phone",
        "user.username",
        "user.email",
        "first_name",
        "last_name",
    ]
