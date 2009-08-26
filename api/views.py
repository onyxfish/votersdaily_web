import json
import urllib
import urllib2

import couchdb
from couchdb.client import PermanentView, uri
from django.http import HttpResponse, HttpResponseRedirect, Http404

from votersdaily_web import settings

def couchdb_urlopen(server, database, design, view, **options):
    """
    Build a CouchDB view url, open it, and return the raw results.
    
    TODO: handle options
    """
    url = '%s/%s/_design/%s/_view/%s' % (server, database, design, view)
    
    return urllib2.urlopen(url)

def events_all(request):
    """
    Return all events in the database.
    """
    
    # JSON
    #if request.accepts('application/json'):
        # GET
    if request.method == 'GET':
        #try:
        json_result = couchdb_urlopen(
            settings.COUCHDB_SERVER_URI, 
            settings.COUCHDB_EVENTDB_NAME, 
            'api', 
            'all')
        #except HttpError:
            #TODO
            
        return HttpResponse(json_result, mimetype='application/json')
    else:
        raise NotImplementedError()
    #else:
    #    raise NotImplementedError()

def events_branch(request, branch):
    """
    Return the events for a specific branch of government, using a pre-
    generated view.
    """
    
    # JSON
    #if request.accepts('application/json'):
        # GET
    if request.method == 'GET':        
        #try:
        json_result = couchdb_urlopen(
            settings.COUCHDB_SERVER_URI, 
            settings.COUCHDB_EVENTDB_NAME, 
            'api', 
            urllib.quote(branch))
        #except HttpError:
            #TODO

        return HttpResponse(json_result, mimetype='application/json')
    else:
        raise NotImplementedError()
    #else:
    #    raise NotImplementedError()

def events_entity(request, entity):
    """
    Return the events for a specific government entity, using a pre-generated 
    view.
    """
    
    # JSON
    #if request.accepts('application/json'):
        # GET
    if request.method == 'GET':
        #try:        
        json_result = couchdb_urlopen(
            settings.COUCHDB_SERVER_URI, 
            settings.COUCHDB_EVENTDB_NAME, 
            'api',
            urllib.quote(entity))
        
            #'/_design/api/_view/executive?startkey="2009-08"&descending=true'))
        #except HttpError:
            #TODO
            #

#

        return HttpResponse(json_result, mimetype='application/json')
    else:
        raise NotImplementedError()
    #else:
    #    raise NotImplementedError()
    