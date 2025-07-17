import pytest

from tests.accounts.factories import ProfileFactory
from tests.fixtures.user import fake_user


@pytest.fixture
def fake_profile(fake_user):
    return ProfileFactory(user=fake_user)
