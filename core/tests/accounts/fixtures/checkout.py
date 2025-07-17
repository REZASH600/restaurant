import pytest
from tests.accounts.factories import CheckoutFactory





@pytest.fixture
def default_checkout(fake_profile):
    return CheckoutFactory(user_profile=fake_profile, is_default=True)

@pytest.fixture
def second_default_checkout(fake_profile):
    return CheckoutFactory(user_profile=fake_profile, is_default=True)

@pytest.fixture
def non_default_checkout(fake_profile):
    return CheckoutFactory(user_profile=fake_profile, is_default=False)