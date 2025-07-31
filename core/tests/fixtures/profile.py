import pytest

from tests.accounts.factories import ProfileFactory



@pytest.fixture
def normal_user_profile(normal_user):
    return ProfileFactory(user=normal_user)



@pytest.fixture
def admin_user_profile(admin_user):
    return ProfileFactory(user=admin_user)
