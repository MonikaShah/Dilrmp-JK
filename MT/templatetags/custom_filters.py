from django import template

register = template.Library()

@register.filter
def pretty_label(value):
    return value.replace("_", " ").title()

@register.filter
def get_field(obj, field_name):
    try:
        return getattr(obj, field_name)
    except AttributeError:
        return ''
    
@register.filter
def replace(value, arg):
    """Replaces all occurrences of the first char with the second."""
    old, new = arg.split(',')  # Split the comma-separated arguments
    return value.replace(old, new)

@register.filter
def getattribute(obj, attr):
    return getattr(obj, attr, '')

@register.filter
def get_item(dictionary, key):
    """Retrieve a value from a dictionary by key."""
    if dictionary is not None and key is not None:
        return dictionary.get(key)
    return None