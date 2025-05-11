from celery import shared_task
from django.db.models import Avg
from apps.menus.models import MenuItems
import logging

from django.core.cache import cache


logger = logging.getLogger(__name__)


@shared_task(queue="tasks")
def update_menu_item_ratings():
    """
    Periodically update the ratings of all menu items in the database and cache.
    """
    menu_items = MenuItems.objects.all()
    for menu_item in menu_items:
        avg_rate = menu_item.reviews.aggregate(avg=Avg("rate"))["avg"] or 0

        # Update the average rating in the database
        menu_item.rate = round(avg_rate, 2)
        menu_item.save()

        # Update the cache for the menu item
        key = f"menu_item_rating_{menu_item.id}"
        data = {
            "sum": menu_item.rate,  
            "count": menu_item.reviews.count(),  
            "avg": round(avg_rate, 2),  
        }
        cache.set(key, data, timeout=86400)
