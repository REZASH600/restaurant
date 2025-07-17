import pytest
from django.db import IntegrityError
from apps.branches.models import RestaurantOpeningHours

@pytest.mark.django_db
class TestRestaurantOpeningHoursModel:

    def test_str_when_open(self, opening_hour_tuesday_open):
        ro = opening_hour_tuesday_open
        expected = f"{ro.restaurant.name} - Tuesday | 08:30 to 16:45"
        assert str(ro) == expected

    def test_str_when_closed(self, opening_hour_wednesday_closed):
        ro = opening_hour_wednesday_closed
        expected = f"{ro.restaurant.name} - Wednesday - Closed"
        assert str(ro) == expected

    def test_unique_together_constraint(self, restaurant):
        ro1 = RestaurantOpeningHours.objects.create(
            restaurant=restaurant,
            day=RestaurantOpeningHours.WeekDays.THURSDAY,
            is_closed=False,
            open_time="09:00",
            close_time="17:00",
        )
        with pytest.raises(IntegrityError):
            RestaurantOpeningHours.objects.create(
                restaurant=restaurant,
                day=RestaurantOpeningHours.WeekDays.THURSDAY,
                is_closed=False,
                open_time="10:00",
                close_time="18:00",
            )

    def test_ordering_by_day(self, restaurant):
        days = list(
            RestaurantOpeningHours.objects.filter(restaurant=restaurant)
            .order_by("day")
            .values_list("day", flat=True)
        )
        assert days == sorted(days)

    def test_is_closed_flag(self, opening_hour_tuesday_open, opening_hour_wednesday_closed):
        assert not opening_hour_tuesday_open.is_closed
        assert opening_hour_wednesday_closed.is_closed

    def test_open_close_times_when_open(self, opening_hour_tuesday_open):
        ro = opening_hour_tuesday_open
        assert ro.open_time is not None
        assert ro.close_time is not None
        assert ro.is_closed is False

    def test_open_close_times_when_closed(self, opening_hour_wednesday_closed):
        ro = opening_hour_wednesday_closed
        assert ro.open_time is None
        assert ro.close_time is None
        assert ro.is_closed is True

    def test_str_edge_cases(self, opening_hour_sunday_midnight, opening_hour_saturday_noon):
        ro_midnight = opening_hour_sunday_midnight
        expected_midnight = f"{ro_midnight.restaurant.name} - Sunday | 00:00 to 12:00"
        assert str(ro_midnight) == expected_midnight

        ro_noon = opening_hour_saturday_noon
        expected_noon = f"{ro_noon.restaurant.name} - Saturday | 12:00 to 23:59"
        assert str(ro_noon) == expected_noon

    def test_closed_trait(self, closed_hours):
        ro = closed_hours
        assert ro.is_closed is True
        assert ro.open_time is None
        assert ro.close_time is None

    def test_all_days_open(self, all_days_open_hours):
        for ro in all_days_open_hours:
            assert ro.is_closed is False
            assert ro.open_time.hour == 9
            assert ro.close_time.hour == 17