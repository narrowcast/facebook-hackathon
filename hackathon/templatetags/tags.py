import json

from django import template
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe

register = template.Library()

# See https://developers.facebook.com/docs/reference/ads-api/currencies/
SUPPORTED_CURRENCIES = {
    'EUR': {'symbol': '\xe2\x82\xac', 'offset': 100},
    'KRW': {'symbol': '\xe2\x82\xa9', 'offset': 1},
    'TWD': {'symbol': 'NT$', 'offset': 1},
    'USD': {'symbol': '$', 'offset': 100},
}


@register.simple_tag
def active(path, url):
    """Returns active if the path is in the given url."""
    if path == reverse_lazy(url):
        return 'active'
    else:
        return ''

@register.filter
def currency(value, currency):
    """Returns the formatted currency."""
    symbol = SUPPORTED_CURRENCIES[currency]['symbol']
    offset = SUPPORTED_CURRENCIES[currency]['offset']
    value = float(value)
    if offset == 100:
        value /= 100.0
        return symbol + '{0:,.2f}'.format(value)
    else:
        return symbol + '{0:,.0f}'.format(value)

@register.filter
def as_json(data):
    """Returns the data encoded in json for use in Javascript."""
    return mark_safe(json.dumps(data))
