from django import template
register = template.Library()


@register.filter
def dict_key(d, key):
    try:
        return d[str(key)]
    except (KeyError, TypeError):
        return ''
