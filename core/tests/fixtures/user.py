import pytest
from tests.accounts.factories import UserFactory


@pytest.fixture
def normal_user():
    return UserFactory(normal=True)


@pytest.fixture
def inactive_user():
    return UserFactory(not_active=True)


@pytest.fixture
def personnel_user():
    return UserFactory(personnel=True)


@pytest.fixture
def admin_user():
    return UserFactory(admin=True)
