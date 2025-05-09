from django.contrib import admin
from .models import Category, MenuItems, MenuItemImages, Reviews


class MenuItemsImagesInline(admin.TabularInline):
    model = MenuItemImages
    extra = 1
    readonly_fields = ["created_at", "updated_at"]


@admin.register(MenuItems)
class MenuItemsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_restaurants",
        "get_categories",
        "price",
        "is_available",
        "stock_quantity",
        "rate",
    )
    list_filter = ("is_available", "restaurant", "category")
    search_fields = ("name", "description")
    list_editable = ("is_available", "stock_quantity", "rate")
    inlines = [MenuItemsImagesInline]
    filter_horizontal = ("category", "restaurant")

    def get_restaurants(self, obj):
        return ", ".join([r.name for r in obj.restaurant.all()])

    get_restaurants.short_description = "Restaurants"

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])

    get_categories.short_description = "Categories"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "get_restaurants")
    search_fields = ("name", "description")
    filter_horizontal = ("restaurant",)

    def get_restaurants(self, obj):
        return ", ".join([r.name for r in obj.restaurant.all()])

    get_restaurants.short_description = "Restaurants"


@admin.register(MenuItemImages)
class MenuItemImagesAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "image_file", "created_at")


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "user_profile", "rate", "short_comment", "created_at")
    search_fields = ("comment", "user_profile__user__username", "menu_item__name")
    list_editable = ("rate",)

    def short_comment(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment

    short_comment.short_description = "Comment"
