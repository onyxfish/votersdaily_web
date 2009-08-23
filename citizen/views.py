import json

import couchdb
from couchdb.schema import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from votersdaily_web import settings
        
def get_event_db():
    """
    Setup CouchDB.  Encapsulated for clarity.
    """
    server = couchdb.Server(settings.COUCHDB_SERVER_URI)
    event_db = server[settings.COUCHDB_EVENTDB_NAME]
    
    return event_db

def all(request):
    """
    Renders a list of all documents.
    """
    event_db = get_event_db()
    
    # GET
    if request.method == 'GET':
        result = event_db.view('api/all')
                
        return render_to_response('all.html', { 'documents': result }) 
    else:
        raise NotImplementedError()
    