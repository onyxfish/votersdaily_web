import json
import urllib
import urllib2

import couchdb
from django.http import HttpResponse, HttpResponseRedirect, Http404

from votersdaily_web import settings

def couchdb_urlopen(server, database, design, view, format, **options):
    """
    Build a CouchDB view url, open it, and return the raw results.
    """
    query = urllib.urlencode(options)
    
    if format == 'json':
        url = '%s/%s/_design/%s/_view/%s?%s' % (
            server, database, design, view, query)
    elif format == 'ical':
        url = '%s/%s/_design/%s/_list/ical/%s?%s' % (
            server, database, design, view, query)
    else:
        raise Http404
    
    return urllib2.urlopen(url)

def get_query_options(request):
    """
    Parses query options common to all API views from a request's GET dict.
    """
    options = {}
    
    try:
        options['endkey'] = request.GET['start']
    except KeyError:
        pass
    
    try:
        options['startkey'] = request.GET['end']
    except KeyError:
        pass
    
    options['descending'] = 'true'
    options['inclusive_start'] = 'true'
    options['inclusive_end'] = 'false'
    
    return options

def get_result_format_and_mimetype(request):
    """
    Determine the format and mimetype from the URL GET parameters.
    """
    format = request.GET.get('format', 'json')
    
    if format == 'json':
        mimetype = 'application/json'
    elif format == 'ical':
        mimetype = 'text/calendar'
    else:
        raise Http404()
    
    return (format, mimetype)

def events_all(request):
    """
    Return all events in the database.
    """
    if request.method != 'GET':
        raise Http404
    
    options = get_query_options(request)    
    format, mimetype = get_result_format_and_mimetype(request)
    
    result = couchdb_urlopen(
        settings.COUCHDB_SERVER_URI, 
        settings.COUCHDB_EVENTDB_NAME, 
        'api', 
        'all',
        format,
        **options)
    
    return HttpResponse(result, mimetype)

def events_branch(request, branch):
    """
    Return the events for a specific branch of government, using a pre-
    generated view.
    """
    if request.method != 'GET':
        raise Http404
    
    options = get_query_options(request)    
    format, mimetype = get_result_format_and_mimetype(request)
    
    result = couchdb_urlopen(
        settings.COUCHDB_SERVER_URI, 
        settings.COUCHDB_EVENTDB_NAME, 
        'api', 
        urllib.quote(branch),
        format,
        **options)

    return HttpResponse(result, mimetype)

def events_entity(request, entity):
    """
    Return the events for a specific government entity, using a pre-generated 
    view.
    """
    if request.method != 'GET':
        raise Http404
    
    options = get_query_options(request)    
    format, mimetype = get_result_format_and_mimetype(request)

    result = couchdb_urlopen(
        settings.COUCHDB_SERVER_URI, 
        settings.COUCHDB_EVENTDB_NAME, 
        'api',
        urllib.quote(entity),
        format,
        **options)

    return HttpResponse(result, mimetype)
    