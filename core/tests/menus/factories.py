from faker import Faker
import factory
from apps.menus import models
from tests.accounts.factories import ProfileFactory

faker = Faker("fa_IR")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category
        skip_postgeneration_save = True

    name = factory.LazyAttribute(lambda _: faker.company())
    description = factory.LazyAttribute(lambda _: faker.text())
    image_file = None

    @factory.post_generation
    def restaurant(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for restaurant in extracted:
                self.restaurant.add(restaurant)


class MenuItemsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MenuItems
        skip_postgeneration_save = True

    name = factory.LazyAttribute(lambda _: faker.word())
    description = factory.LazyAttribute(lambda _: faker.text())
    price = factory.LazyAttribute(
        lambda _: round(
            faker.pydecimal(
                left_digits=3, right_digits=2, positive=True, min_value=0.01
            ),
            2,
        )
    )
    is_available = True
    preparation_time = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=60))
    rate = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=5.0),
            2,
        )
    )
    stock_quantity = factory.LazyAttribute(lambda _: faker.random_int(min=0, max=100))

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.category.add(category)

    @factory.post_generation
    def restaurant(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for restaurant in extracted:
                self.restaurant.add(restaurant)


class MenuItemImagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.MenuItemImages

    image_file = factory.django.ImageField(color="blue")
    menu_item = factory.SubFactory(MenuItemsFactory)


class ReviewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Reviews

    comment = factory.LazyAttribute(lambda _: faker.text())
    rate = factory.LazyAttribute(
        lambda _: round(
            faker.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=5.0),
            2,
        )
    )
    is_published = True




class UserFavoriteMenuItemsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserFavoriteMenuItems
        django_get_or_create = ("user_profile", "menu_item")

    user_profile = factory.SubFactory(ProfileFactory)
    menu_item = factory.SubFactory(MenuItemsFactory)