import factory
from faker import Faker
from factory.django import mute_signals
from django.db.models.signals import post_save
from apps.accounts.models import MyUser, Profile, Checkout

faker = Faker("fa_IR")


def fake_farsi_phone_number():
    return f"09{str(faker.random_number(digits=9, fix_len=True))}"


@mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyUser
        skip_postgeneration_save = True

    phone = factory.LazyFunction(fake_farsi_phone_number)
    username = factory.LazyAttribute(lambda x: faker.user_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    is_phone_verified = True
    password = factory.PostGenerationMethodCall("set_password", "Reza.sh1382")

    class Params:
        normal = factory.Trait(is_active=True, is_staff=False, is_superuser=False)
        not_active = factory.Trait(is_active=False, is_staff=False, is_superuser=False)
        staff = factory.Trait(is_active=True, is_staff=True, is_superuser=False)
        superuser = factory.Trait(is_active=True, is_staff=True, is_superuser=True)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    reviews_count = 0
    orders_count = 0
    temporary_email = factory.LazyAttribute(lambda x: faker.email())


class CheckoutFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Checkout

    user_profile = factory.SubFactory(ProfileFactory)
    address = factory.LazyAttribute(lambda _: faker.address())
    city = factory.LazyAttribute(lambda _: faker.city())
    state = factory.LazyAttribute(lambda _: faker.state())
    postal_code = factory.LazyAttribute(
        lambda _: f"{faker.random_number(digits=10, fix_len=True)}"
    )
    recipient_phone = factory.LazyAttribute(
        lambda _: f"09{faker.random_number(digits=9, fix_len=True)}"
    )
    recipient_name = factory.LazyAttribute(lambda _: faker.name())
    is_default = False
