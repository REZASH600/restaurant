import pytest
from tests.accounts.factories import  UserFactory

@pytest.fixture
def fake_user():
    return UserFactory()


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