import factory
from faker import Faker
from apps.branches.models import Restaurant, RestaurantOpeningHours
from datetime import time

faker = Faker("fa_IR")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.LazyAttribute(lambda _: faker.company())
    description = factory.LazyAttribute(lambda _: faker.text())
    logo = None
    address = factory.LazyAttribute(lambda _: faker.address())
    city = factory.LazyAttribute(lambda _: faker.city())
    postal_code = factory.Sequence(lambda n: f"{5432100000 + n}")
    phone_number1 = factory.Sequence(lambda n: f"0912123{n:04d}")
    phone_number2 = factory.Sequence(lambda n: f"021{4000 + n:04d}")
    email = factory.LazyAttribute(lambda _: faker.email())
    website = factory.LazyAttribute(lambda _: faker.url())

    rate = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=5.0),
            2,
        )
    )
    latitude = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(
                left_digits=2,
                right_digits=6,
                positive=False,
                min_value=-90.0,
                max_value=90.0,
            ),
            6,
        )
    )
    longitude = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(
                left_digits=3,
                right_digits=6,
                positive=False,
                min_value=-180.0,
                max_value=180.0,
            ),
            6,
        )
    )
    support_of_range_delivery = True

    out_of_range_delivery_fee = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(
                left_digits=4, right_digits=2, positive=True, max_value=9999.99
            ),
            2,
        )
    )
    max_out_of_range_distance = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(
                left_digits=2, right_digits=2, positive=True, max_value=99.99
            ),
            2,
        )
    )

    class Params:
        without_optional_fields = factory.Trait(
            phone_number2=None,
            email=None,
        )
        static_test_values = factory.Trait(
            name=factory.LazyAttribute(lambda _: "Test"),
            description=factory.LazyAttribute(lambda _: "Test Description"),
            address=factory.LazyAttribute(lambda _: "Test Address"),
            city=factory.LazyAttribute(lambda _: "Test City"),
            postal_code="5432110000",
            phone_number1="09121234568",
            website="http://example.com",
            latitude=30.0,
            longitude=50.0,
            rate=4.1,
        )


class RestaurantOpeningHoursFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RestaurantOpeningHours

    restaurant = factory.SubFactory(RestaurantFactory)
    day = 0  # Monday
    open_time = time(9, 0)  # 09:00 A.M
    close_time = time(17, 0)  # 05:00 P.M
    is_closed = False

    class Params:
        closed = factory.Trait(
            is_closed=True,
            open_time=None,
            close_time=None,
        )
        tuesday_open = factory.Trait(
            day=RestaurantOpeningHours.WeekDays.TUESDAY,
            is_closed=False,
            open_time=time(8, 30),
            close_time=time(16, 45),
        )
        wednesday_closed = factory.Trait(
            day=RestaurantOpeningHours.WeekDays.WEDNESDAY,
            is_closed=True,
            open_time=None,
            close_time=None,
        )
        sunday_midnight = factory.Trait(
            day=RestaurantOpeningHours.WeekDays.SUNDAY,
            is_closed=False,
            open_time=time(0, 0),
            close_time=time(12, 0),
        )
        saturday_noon = factory.Trait(
            day=RestaurantOpeningHours.WeekDays.SATURDAY,
            is_closed=False,
            open_time=time(12, 0),
            close_time=time(23, 59),
        )
