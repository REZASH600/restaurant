from django.db import models
from django.utils.translation import gettext_lazy as _
from utils import validations
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.cache import cache
from django.db.models import Avg


class Restaurant(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    logo = models.ImageField(
        null=True, blank=True, upload_to="branches/logo", verbose_name=_("logo")
    )
    address = models.TextField(verbose_name=_("address"))
    city = models.CharField(max_length=100, verbose_name=_("city"))
    postal_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[validations.custom_postal_code_validator],
        verbose_name=_("postal code"),
    )

    phone_number1 = models.CharField(
        max_length=11,
        unique=True,
        validators=[validations.validate_phone],
        verbose_name=_("phone number1"),
    )

    phone_number2 = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("phone number2 (mobile or landline)"),
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("email address"),
    )
    website = models.URLField(verbose_name=_("website"))
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        verbose_name=_("rate"),
    )

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("latitude")
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("longitude")
    )

    support_of_range_delivery = models.BooleanField(
        default=True, verbose_name=_("supports delivery in range")
    )

    out_of_range_delivery_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("out of range delivery fee"),
    )

    max_out_of_range_distance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name=_("max out of range distance (km)"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    @property
    def is_open_now(self):
        now = timezone.localtime()
        current_day = now.weekday()

        opening_hour = self.opening_hours.filter(
            day=current_day, is_closed=False
        ).first()

        if not opening_hour:
            return False

        now_time = now.time()
        return opening_hour.open_time <= now_time <= opening_hour.close_time

    def get_cached_rate(self):

        key = f"restaurant_rating_{self.id}"
        data = cache.get(key)
        return round(data["avg"], 2) if data else self.rate

    def __str__(self):
        return f"{self.name}:{self.description}"

    class Meta:
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurants")


class RestaurantOpeningHours(models.Model):
    class WeekDays(models.IntegerChoices):
        MONDAY = 0, _("Monday")
        TUESDAY = 1, _("Tuesday")
        WEDNESDAY = 2, _("Wednesday")
        THURSDAY = 3, _("Thursday")
        FRIDAY = 4, _("Friday")
        SATURDAY = 5, _("Saturday")
        SUNDAY = 6, _("Sunday")

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="opening_hours",
        verbose_name=_("Restaurant"),
    )

    day = models.IntegerField(
        choices=WeekDays.choices, verbose_name=_("Day of the Week")
    )

    open_time = models.TimeField(verbose_name=_("Opening Time"), null=True, blank=True)

    close_time = models.TimeField(verbose_name=_("Closing Time"), null=True, blank=True)

    is_closed = models.BooleanField(default=False, verbose_name=_("Closed on this day"))

    def __str__(self):
        day_name = self.get_day_display()
        restaurant_name = self.restaurant.name
        if self.is_closed:
            return f"{restaurant_name} - {day_name} - Closed"
        return f"{restaurant_name} - {day_name} | {self.open_time.strftime('%H:%M')} to {self.close_time.strftime('%H:%M')}"

    class Meta:
        unique_together = ("restaurant", "day")
        verbose_name = _("Restaurant Opening Hour")
        verbose_name_plural = _("Restaurant Opening Hours")
        ordering = ["restaurant", "day"]
