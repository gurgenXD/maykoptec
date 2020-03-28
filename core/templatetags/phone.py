from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def only_digits(value):
    import re
    return re.sub(r'\D', '', value)

register.filter('only_digits', only_digits)