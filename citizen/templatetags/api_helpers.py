import datetime

from django import template
from django.template.defaultfilters import stringfilter

"""
This module holds Django tags and filters that aid in formatting for display
the output of the API.
"""

register = template.Library()

@register.filter(name='iso8601')
@stringfilter
def iso8601(value, format):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime(format)
    except:
        return ''