import pytest
from apps.accounts.models import Checkout
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestCheckoutModel:

    def test_str_representation(self, default_checkout):
        expected = f"Checkout for {default_checkout.recipient_name} - {default_checkout.address}"
        assert str(default_checkout) == expected

    def test_field_values_are_assigned(self, default_checkout):
        assert default_checkout.address
        assert default_checkout.city
        assert default_checkout.state
        assert len(default_checkout.postal_code) == 10
        assert default_checkout.recipient_name
        assert default_checkout.recipient_phone.startswith("09")

    def test_signal_sets_only_one_default(self, normal_user_profile, default_checkout, second_default_checkout):
        default_checkout.refresh_from_db()
        second_default_checkout.refresh_from_db()

        defaults = Checkout.objects.filter(user_profile=normal_user_profile, is_default=True)
        assert defaults.count() == 1
        assert second_default_checkout in defaults
        assert not default_checkout.is_default

    def test_multiple_non_default_checkouts_allowed(self, non_default_checkout):
        all_checkouts = Checkout.objects.filter(user_profile=non_default_checkout.user_profile)
        assert all(c.is_default is False for c in all_checkouts)

    @pytest.mark.parametrize("invalid_code", ["123", "abc", "1234567a", "12345678901"])
    def test_invalid_postal_code_raises(self, normal_user_profile, invalid_code):
        checkout = Checkout(
            user_profile=normal_user_profile,
            address="Some address",
            city="Tehran",
            state="Tehran",
            postal_code=invalid_code,
            recipient_phone="09123456789",
            recipient_name="Ali"
        )
        with pytest.raises(ValidationError):
            checkout.full_clean()
