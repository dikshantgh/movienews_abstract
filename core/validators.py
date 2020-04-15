# core/validators.py
from django.core.exceptions import ValidationError
import re


def phone_number_validator(value):
    check = re.compile(r'^\d{10}$')
    if not check.match(value):
        raise ValidationError("Enter a valid number")
    return value
