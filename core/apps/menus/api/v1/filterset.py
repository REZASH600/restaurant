from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django_filters import rest_framework as filters
from apps.menus.models import MenuItems


class MenuItemFilter(filters.FilterSet):

    search = filters.CharFilter(method="filter_search")

    price = filters.RangeFilter()

    is_available = filters.BooleanFilter(field_name="is_available")

    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    preparation_time = filters.NumericRangeFilter(field_name="preparation_time")
    
    rate = filters.NumericRangeFilter(
        field_name="rate",
        help_text="Filter menu items with rating between 1 and 5",
    )

    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = MenuItems
        fields = [
            "search",
            "price",
            "is_available",
            "category",
            "preparation_time",
            "rate",
            "created_at",
            "updated_at",
        ]

    def filter_search(self, queryset, name, value):
        return (
            queryset.annotate(
                sim_name=TrigramSimilarity("name", value),
                sim_desc=TrigramSimilarity("description", value),
                sim_category=TrigramSimilarity("category__name", value),
                similarity=Greatest("sim_name", "sim_desc", "sim_category"),
            )
            .filter(similarity__gt=0.3)
            .order_by("-similarity")
        )
