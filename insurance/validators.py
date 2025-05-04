import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_iranian_phone(value):
    pattern = r"^(?:\+98|0)?9\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError(
            _(
                "Invalid phone number format. Valid formats: +989xxxxxxxxx, 09xxxxxxxxx, or 9xxxxxxxxx"
            ),
            code="invalid_phone",
        )

def normalize_iranian_phone(value: str) -> str:
    if value.startswith('0'):
        return '+98' + value[1:]
    elif value.startswith('9'):
        return '+98' + value
    return value  


def validate_and_normalize_id_card(value: str) -> str:
    if not value.isdigit():
        raise ValidationError(
            _("ID card must contain only digits."), code="invalid_id_card"
        )

    if len(value) > 10:
        raise ValidationError(
            _("ID card must be at most 10 digits long."), code="invalid_length"
        )

    return value.zfill(10)