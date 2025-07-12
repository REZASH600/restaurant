from django.contrib import admin

from . import models


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    search_fields = ("name", "city", "postal_code", "phone_number1", "email")
    list_filter = ("city", "rate", "support_of_range_delivery")


@admin.register(models.RestaurantOpeningHours)
class RestaurantOpeningHoursAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant",
        "get_day_display",
        "open_time",
        "close_time",
        "is_closed",
    )
    search_fields = ("restaurant__name", "restaurant__id")
    list_filter = ("restaurant", "is_closed", "day")
    list_editable = ("open_time", "close_time", "is_closed")
