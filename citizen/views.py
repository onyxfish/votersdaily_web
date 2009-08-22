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
    event_db = get_event_db()
    
    # JSON
    #if request.accepts('application/json'):
        # GET
    if request.method == 'GET':
        #doc_id = '2008-10-06T00:00:00Z - Judicial - Supreme Court - Order List'
        #document = event_db[doc_id]
        
        documents = []
        
        for doc_id in event_db:
            documents.append(event_db[doc_id])
                
        return render_to_response('all.html', { 'documents': documents }) 
    else:
        raise NotImplementedError()
    # HTML
    #else:
    #    raise NotImplementedError()
    