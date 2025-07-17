import pytest

from tests.accounts.factories import ProfileFactory



@pytest.fixture
def fake_profile(fake_user):
    return ProfileFactory(user=fake_user)
