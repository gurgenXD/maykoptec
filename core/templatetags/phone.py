import re
from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def only_digits(value):
    if value:
        return re.sub(r'\D', '', value)

register.filter('only_digits', only_digits)


@register.filter
@stringfilter
def phone_code(value):
    if value:
        return value.split(')')[0] + ')'

register.filter('phone_code', phone_code)


@register.filter
@stringfilter
def phone_nmb(value):
    if len(value.split(')')) > 1:
        return value.split(')')[1]

register.filter('phone_nmb', phone_nmb)
