import json

import couchdb
from couchdb.client import PermanentView, uri
from django.http import HttpResponse, HttpResponseRedirect, Http404

from votersdaily_web import settings
        
def get_event_db():
    """
    Setup CouchDB.  Encapsulated for clarity.
    """
    server = couchdb.Server(settings.COUCHDB_SERVER_URI)
    event_db = server[settings.COUCHDB_EVENTDB_NAME]
    
    return event_db

def get_view_results(database, name):
    """
    Hacky method to get a dict of results from a couchdb-python View.
    
    See couchdb.client.Database.view.
    """          
    if not name.startswith('_'):
        design, name = name.split('/', 1)
        name = '/'.join(['_design', design, '_view', name])
    
    view = PermanentView(
        uri(database.resource.uri, *name.split('/')), 
        name,
        wrapper=None,
        http=database.resource.http)
        
    return view._exec({})

def events_all(request):
    """
    Return all events in the database.
    """
    
    # JSON
    #if request.accepts('application/json'):
        # GET
    if request.method == 'GET':
        event_db = get_event_db()
            
        result = get_view_results(event_db, 'api/all')
        json_result = json.dumps(result)
            
        return HttpResponse(json_result, mimetype='application/json')
    else:
        raise NotImplementedError()
    #else:
    #    raise NotImplementedError()
    