import json
import urllib
import urllib2

import couchdb
from django.http import HttpResponse, HttpResponseRedirect, Http404

from votersdaily_web import settings

def couchdb_urlopen(server, database, design, view, **options):
    """
    Build a CouchDB view url, open it, and return the raw results.
    """
    query = urllib.urlencode(options)
    url = '%s/%s/_design/%s/_view/%s?%s' % (
        server, database, design, view, query)
    
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

def events_all(request):
    """
    Return all events in the database.
    """
    if request.method != 'GET':
        raise Http404
    
    options = get_query_options(request)
    
    # TODO - support alternate formats
    format = request.GET.get('format', 'json')
    
    json_result = couchdb_urlopen(
        settings.COUCHDB_SERVER_URI, 
        settings.COUCHDB_EVENTDB_NAME, 
        'api', 
        'all',
        **options)
            
    return HttpResponse(json_result, mimetype='application/json')

def events_branch(request, branch):
    """
    Return the events for a specific branch of government, using a pre-
    generated view.
    """
    if request.method != 'GET':
        raise Http404
    
    options = get_query_options(request)
    
    # TODO - support alternate formats
    format = request.GET.get('format', 'json')
    
    json_result = couchdb_urlopen(
        settings.COUCHDB_SERVER_URI, 
        settings.COUCHDB_EVENTDB_NAME, 
        'api', 
        urllib.quote(branch),
        **options)

    return HttpResponse(json_result, mimetype='application/json')

def events_entity(request, entity):
    """
    Return the events for a specific government entity, using a pre-generated 
    view.
    """
    if request.method != 'GET':
        raise Http404
    
    options = get_query_options(request)
    
    # TODO - support alternate formats
    format = request.GET.get('format', 'json')

    json_result = couchdb_urlopen(
        settings.COUCHDB_SERVER_URI, 
        settings.COUCHDB_EVENTDB_NAME, 
        'api',
        urllib.quote(entity),
        **options)

    return HttpResponse(json_result, mimetype='application/json')
    