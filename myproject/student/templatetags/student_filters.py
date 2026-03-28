# student/templatetags/student_filters.py
from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Safely get value from dictionary by key (as string)."""
    if not d:
        return ""
    return d.get(str(key), "")
