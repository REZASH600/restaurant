from celery import shared_task
from django.db.models import Avg
from apps.branches.models import Restaurant
from django.core.cache import cache


@shared_task(queue="tasks")
def update_restaurant_ratings():
    """
    Periodically update the restaurant ratings in the database and cache.
    """
    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:

        avg_rate = restaurant.reviews.aggregate(avg=Avg("rate"))["avg"] or 0

        # Update the average rating in the database
        restaurant.rate = round(avg_rate, 2)
        restaurant.save()

        # Update the cache for the restaurant
        key = f"restaurant_rating_{restaurant.id}"
        data = {
            "sum": restaurant.rate,  
            "count": restaurant.reviews.count(), 
            "avg": round(avg_rate, 2),  
        }
        cache.set(key, data, timeout=86400)
