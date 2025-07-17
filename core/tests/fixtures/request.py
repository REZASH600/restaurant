import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def rf():
    return APIRequestFactory()