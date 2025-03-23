from django import template

register = template.Library()

@register.filter
def abs_value(value):
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return value

@register.filter
def is_positive(value):
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False

@register.filter
def is_negative(value):
    try:
        return float(value) < 0
    except (ValueError, TypeError):
        return False