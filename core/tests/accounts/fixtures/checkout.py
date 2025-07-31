import pytest
from tests.accounts.factories import CheckoutFactory





@pytest.fixture
def default_checkout(normal_user_profile):
    return CheckoutFactory(user_profile=normal_user_profile, is_default=True)

@pytest.fixture
def second_default_checkout(normal_user_profile):
    return CheckoutFactory(user_profile=normal_user_profile, is_default=True)

@pytest.fixture
def non_default_checkout(normal_user_profile):
    return CheckoutFactory(user_profile=normal_user_profile, is_default=False)