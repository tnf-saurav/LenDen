from django.core.exceptions import ValidationError
import re

def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits.')
    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 digits long.')