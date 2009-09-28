import datetime

from django import template
from django.template.defaultfilters import stringfilter

"""
This module holds Django tags and filters that aid in formatting for display
the output of the API.
"""

register = template.Library()

@register.filter
@stringfilter
def iso8601(value, format):
    try:
        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime(format)
    except:
        return ''
   
@register.filter
@stringfilter 
def iso8601_pretty(value):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            return dt.strftime('%B %-d, %Y')
        else:
            return dt.strftime('%B %-d, %Y at %-I:%M %p')
    except:
        return ''
    
@register.filter
@stringfilter 
def iso8601_pretty_time(value):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            return ''
        else:
            return dt.strftime('%-I:%M %p')
    except:
        return ''

@register.inclusion_tag('include_branch.html')
def include_branch(branch):
    return { 'branch': branch }