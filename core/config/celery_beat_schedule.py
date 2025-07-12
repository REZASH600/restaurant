from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "update-menu-ratings-nightly": {
        "task": "apps.menus.tasks.menu_rating.update_menu_item_ratings",
        "schedule": crontab(hour=3, minute=0),  # every night at 3 AM
    },
    "update-restaurant-ratings-nightly": {
        "task": "apps.branches.tasks.restaurant_rating.update_restaurant_ratings",
        "schedule": crontab(hour=4, minute=0),  # every night at 4 AM
    },
    "delete-old-favorite-menu-items-nightly": {
        "task": "apps.menus.tasks.cleanup.delete_old_favorite_menu_items",
        "schedule": crontab(hour=5, minute=0),  # every night at 5 AM
    },
}
