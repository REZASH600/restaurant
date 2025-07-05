from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django_filters import rest_framework as filters
from apps.menus.models import MenuItems , Reviews


class MenuItemFilter(filters.FilterSet):

    search = filters.CharFilter(method="filter_search")

    price = filters.RangeFilter()

    is_available = filters.BooleanFilter(field_name="is_available")

    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    category_id = filters.NumberFilter(field_name="category__id")

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
            "category_id",
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




class ReviewFilter(filters.FilterSet):
    rate = filters.RangeFilter()
    menu_item = filters.NumberFilter(field_name="menu_item__id")
    restaurant = filters.NumberFilter(field_name="restaurant__id")
    created_at = filters.DateFromToRangeFilter()
    is_published = filters.BooleanFilter()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and not self.request.user.is_staff:
            self.filters.pop('is_published', None)

    class Meta:
        model = Reviews
        fields = ["rate", "menu_item", "restaurant", "created_at", "is_published"]




class CategoryFilter(filters.FilterSet):

    search = filters.CharFilter(method="filter_search")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")


    class Meta:
        model = MenuItems
        fields = [
            "search",
            "created_at",
            "updated_at",
        ]

    
    def filter_search(self, queryset, name, value):
        return (
            queryset.annotate(
                sim_name=TrigramSimilarity("name", value),
                sim_desc=TrigramSimilarity("description", value),
            )
            .filter(similarity__gt=0.3)
            .order_by("-similarity")
        )