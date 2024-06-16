from django import template

register = template.Library()  # 341
@register.filter
def model_name(obj): # 341
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
