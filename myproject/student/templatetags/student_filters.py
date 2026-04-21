from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """
    Safely get value from dictionary by key.
    Useful for retrieving saved answers from the session.
    """
    if not isinstance(dictionary, dict):
        return ""
    return dictionary.get(str(key), "")

@register.filter
def get_option_text(question, key):
    """
    Maps keys (A, B, C, D or 1, 2, 3, 4) to the model fields.
    """
    if not key or not question:
        return ""
    
    # Map both Letters and Numbers to ensure the 4-option grid never fails
    mapping = {
        'A': 'option_a', '1': 'option_a',
        'B': 'option_b', '2': 'option_b',
        'C': 'option_c', '3': 'option_c',
        'D': 'option_d', '4': 'option_d',
    }
    
    lookup_key = str(key).upper()
    field_name = mapping.get(lookup_key)
    
    if field_name:
        return getattr(question, field_name, "")
    return ""