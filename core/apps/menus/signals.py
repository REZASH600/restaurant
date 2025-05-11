from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.menus.models import Reviews
from apps.menus.utils.cache import update_menu_item_cache, update_restaurant_cache


@receiver(post_save, sender=Reviews)
def update_rating_on_create(sender, instance, created, **kwargs):
    if not created:
        return

    update_menu_item_cache(instance.menu_item.id, instance.rate)
    update_restaurant_cache(instance.restaurant.id, instance.rate)

@receiver(post_delete, sender=Reviews)
def update_rating_on_delete(sender, instance, **kwargs):
    update_menu_item_cache(instance.menu_item.id, -instance.rate)
    update_restaurant_cache(instance.restaurant.id, -instance.rate)