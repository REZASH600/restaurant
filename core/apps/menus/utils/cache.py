from django.core.cache import cache
from apps.branches.models import Restaurant
from apps.menus.models import MenuItems
from django.db.models import Avg
from decimal import Decimal

def update_menu_item_cache(menu_item_id, delta_rate):
    key = f"menu_item_rating_{menu_item_id}"
    data = cache.get(key)

    if data is None:
        menu_item = MenuItems.objects.get(id=menu_item_id)
        avg_rate = menu_item.reviews.aggregate(avg=Avg('rate'))["avg"] or 0
        data = {
            "sum": menu_item.rate, 
            "count": menu_item.reviews.count(), 
            "avg": round(avg_rate, 2),  
        }


    data["sum"] += Decimal(str(delta_rate))
    data["count"] = max(data["count"] + (1 if delta_rate > 0 else -1), 1)
    data["avg"] = round(data["sum"] / data["count"], 2)
    cache.set(key, data, timeout=86400)

def update_restaurant_cache(restaurant_id, delta_rate):
    key = f"restaurant_rating_{restaurant_id}"
    data = cache.get(key)
    if data is None:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        avg_rate = restaurant.reviews.aggregate(avg=Avg('rate'))["avg"] or 0
        data = {
            "sum": restaurant.rate,  
            "count": restaurant.reviews.count(), 
            "avg": round(avg_rate, 2), 
        }
    data["sum"] += Decimal(str(delta_rate))
    data["count"] = max(data["count"] + (1 if delta_rate > 0 else -1), 1)
    data["avg"] = round(data["sum"] / data["count"], 2)
    cache.set(key, data, timeout=86400)