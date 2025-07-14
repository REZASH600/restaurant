import pytest
from apps.accounts.tests.factories import UserFactory, ProfileFactory,CheckoutFactory

@pytest.fixture
def normal_user():
    return UserFactory(normal=True)

@pytest.fixture
def inactive_user():
    return UserFactory(not_active=True)

@pytest.fixture
def staff_user():
    return UserFactory(staff=True)

@pytest.fixture
def super_user():
    return UserFactory(superuser=True)



@pytest.fixture
def default_checkout(fake_profile):
    return CheckoutFactory(user_profile=fake_profile, is_default=True)

@pytest.fixture
def second_default_checkout(fake_profile):
    return CheckoutFactory(user_profile=fake_profile, is_default=True)

@pytest.fixture
def non_default_checkout(fake_profile):
    return CheckoutFactory(user_profile=fake_profile, is_default=False)