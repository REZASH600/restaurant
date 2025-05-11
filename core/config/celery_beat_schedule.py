from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "update-menu-ratings-nightly": {
        "task": "apps.menus.tasks.menu_rating.update_menu_item_ratings",
        "schedule": crontab(hour=3, minute="*"),  # every night at 3 AM
    },
    "update-restaurant-ratings-nightly": {
        "task": "apps.branches.tasks.restaurant_rating.update_restaurant_ratings",
        "schedule": crontab(hour=4, minute="*"),  # every night at 4 AM
    },
}

