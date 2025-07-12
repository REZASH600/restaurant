import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(value):
    """
    Validates that the provided phone number is a valid Iranian mobile or landline number.

    Mobile numbers must start with '09' and be followed by 9 digits.
    Landline numbers must start with '0' followed by an area code and 7 to 8 digits.

    Args:
        value (str): The phone number to validate.

    Raises:
        ValidationError: If the phone number is not in the correct format.
    """
    if value is not None:
        mobile_regex = re.compile(r"^09\d{9}$")         # Matches 09xxxxxxxxx
        landline_regex = re.compile(r"^0[1-8]\d{9}$")   # Matches 0Xxxxxxxxxx (area code + 8 digits)

        if not (mobile_regex.match(value) or landline_regex.match(value)):
            raise ValidationError(_("Please enter a valid Iranian phone or landline number."))


def custom_postal_code_validator(value):
    if not value.isdigit():
        raise ValidationError(_("Postal code must contain only numbers."))
    if len(value) != 10:
        raise ValidationError(_("Iranian postal code must be exactly 10 digits."))