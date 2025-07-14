import pytest
from apps.branches.tests.factories import RestaurantFactory
from apps.accounts.tests.factories import ProfileFactory, UserFactory


@pytest.fixture
def restaurant():
    return RestaurantFactory()


@pytest.fixture
def fake_user():
    return UserFactory()


@pytest.fixture
def fake_profile(fake_user):
    return ProfileFactory(user=fake_user)


@pytest.fixture
def multiple_restaurants():
    return RestaurantFactory.create_batch(3)
