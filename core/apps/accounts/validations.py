import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(value):
    """
    Validates that the provided phone number is a valid Iranian phone number.

    An Iranian phone number must start with '09' and be followed by exactly 9 digits.

    Args:
        value (str): The phone number to validate.

    Raises:
        ValidationError: If the phone number is not in the correct format.
    """
    # Regular expression for validating Iranian phone numbers
    phone_regex = re.compile(r"^(09)\d{9}$")  # Matches "09" followed by 9 digits

    if value is not None:
        if not phone_regex.match(value):
            raise ValidationError(_("Please enter a valid phone number."))


def custom_postal_code_validator(value):
    if not value.isdigit():
        raise ValidationError(_("Postal code must contain only numbers."))
    if len(value) != 10:
        raise ValidationError(_("Iranian postal code must be exactly 10 digits."))