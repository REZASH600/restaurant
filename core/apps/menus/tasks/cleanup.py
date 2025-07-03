from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from menus.models import UserFavoriteMenuItems
import logging


logger = logging.getLogger(__name__)


@shared_task(queue="tasks")
def delete_old_favorite_menu_items():
    threshold_date = timezone.now() - timedelta(days=60)
    old_favorites = UserFavoriteMenuItems.objects.filter(created_at__lt=threshold_date)
    count = old_favorites.count()
    old_favorites.delete()
    return f"Deleted {count} old favorite menu items."