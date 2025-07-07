from rest_framework import generics, permissions as drf_permissions
from apps.branches import models
from . import serializers
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from utils.permissions import IsAdminOrIsPersonnel

class RestaurantListApiView(generics.ListAPIView):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantListSerializer


class RestaurantCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.RestaurantDetailSerializer
    permission_classes = [
        drf_permissions.IsAdminUser,
    ]


class RestaurantUpdateApiView(generics.UpdateAPIView):
    http_method_names = ["patch"]
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantDetailSerializer
    permission_classes = [
        IsAdminOrIsPersonnel,
    ]


class RestaurantRetrieveApiView(generics.RetrieveAPIView):
    queryset = models.Restaurant.objects.all()
    serializer_class = serializers.RestaurantDetailSerializer


class RestaurantOpeningHoursCreateApiView(generics.CreateAPIView):
    queryset = models.RestaurantOpeningHours.objects.all()
    serializer_class = serializers.RestaurantOpeningHoursSerializer
    permission_classes = [IsAdminOrIsPersonnel]


class RestaurantOpeningHoursListApiView(generics.ListAPIView):
    queryset = models.RestaurantOpeningHours.objects.all()
    serializer_class = serializers.RestaurantOpeningHoursSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["restaurant", "day"]
    ordering_fields = ["restaurant", "day", "open_time", "close_time"]


class RestaurantOpeningHoursUpdateApiView(generics.UpdateAPIView):
    http_method_names = ["patch"]
    queryset = models.RestaurantOpeningHours.objects.all()
    serializer_class = serializers.RestaurantOpeningHoursSerializer
    permission_classes = [IsAdminOrIsPersonnel]