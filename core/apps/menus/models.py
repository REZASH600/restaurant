from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.branches.models import Restaurant
from apps.accounts.models import Profile
from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("category name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    image_file = models.ImageField(
        upload_to="categories/", blank=True, null=True, verbose_name=_("image file")
    )

    restaurant = models.ManyToManyField(
        Restaurant,
        related_name="categories",
        blank=True,
        verbose_name=_("restaurant"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class MenuItems(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("item name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("price")
    )

    is_available = models.BooleanField(default=True, verbose_name=_("is available"))
    preparation_time = models.IntegerField(
        default=0, verbose_name=_("preparation time (minutes)")
    )
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("5.0")),
        ],
        default=Decimal("0.0"),
        verbose_name=_("rate"),
    )

    stock_quantity = models.IntegerField(default=0, verbose_name=_("stock quantity"))

    category = models.ManyToManyField(
        Category,
        related_name="menu_items",
        blank=True,
        verbose_name=_("category"),
    )
    restaurant = models.ManyToManyField(
        Restaurant,
        related_name="menu_items",
        blank=True,
        verbose_name=_("restaurant"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def get_cached_rate(self):

        key = f"menu_item_rating_{self.id}"
        data = cache.get(key)
        return round(data["avg"], 2) if data else self.rate

    def __str__(self):
        return f"{self.restaurant}-{self.name}-{self.price}"

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")


class MenuItemImages(models.Model):
    image_file = models.ImageField(
        upload_to="menu_items/", blank=True, null=True, verbose_name=_("image file")
    )
    menu_item = models.ForeignKey(
        MenuItems,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name=_("menu item"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("Menu Item Image")
        verbose_name_plural = _("Menu Item Images")


class Reviews(models.Model):
    comment = models.TextField(verbose_name=_("comment"))
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("5.0")),
        ],
        default=Decimal("0.0"),
        verbose_name=_("rate"),
    )
    user_profile = models.ForeignKey(
        Profile,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("user profile"),
    )
    menu_item = models.ForeignKey(
        MenuItems,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("menu item"),
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("restaurant"),
    )
    is_published = models.BooleanField(default=True, verbose_name=_("is published"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def __str__(self):
        return f"{self.user_profile}-{self.menu_item}-{self.comment}"

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class UserFavoriteMenuItems(models.Model):
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="favorite_menu_items",
        verbose_name=_("user profile"),
    )
    menu_item = models.ForeignKey(
        MenuItems,
        on_delete=models.CASCADE,
        related_name="favorite_menu_items",
        verbose_name=_("menu item"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        unique_together = ("user_profile", "menu_item")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user_profile"]),
            models.Index(fields=["menu_item"]),
            models.Index(fields=["user_profile", "menu_item"]),
        ]

        verbose_name = _("User Favorite Menu Item")
        verbose_name_plural = _("User Favorite Menu Items")

    def __str__(self):
        return f"{self.user_profile} likes {self.menu_item}"
