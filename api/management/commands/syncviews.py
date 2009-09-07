import os
import re

import couchdb
from couchdb.design import ViewDefinition
from django.core.management.base import NoArgsCommand

from votersdaily_web import settings


class Command(NoArgsCommand):
    help = 'Synchronize views defined in the API to CouchDB.'
        
    def sync_event_views(self, event_db):
        """
        Import ViewDefinitions for the event database and sync them.        
        """
        print 'Importing view maker functions'
        
        # Import all view generator functions from the couchdb.views module
        from votersdaily_web.api.couchdb import event_views
        view_makers = [
            v for k, v in event_views.__dict__.items() if k.find('make_views') == 0]
        
        view_definitions = []
        
        for maker in view_makers:
            print 'Executing %s()' % maker.__name__
            view_definitions.extend(maker(event_db))
        
        print 'Syncing a total of %i views to CouchDB' % len(view_definitions)
        ViewDefinition.sync_many(
            event_db, view_definitions, remove_missing=True)
        
        print 'Finished'
        
    def sync_log_views(self, log_db):
        """
        Import ViewDefinitions for the log database and sync them.        
        """
        print 'Importing view maker functions'
        
        # Import all view generator functions from the couchdb.views module
        from votersdaily_web.api.couchdb import log_views
        view_makers = [
            v for k, v in log_views.__dict__.items() if k.find('make_views') == 0]
        
        view_definitions = []
        
        for maker in view_makers:
            print 'Executing %s()' % maker.__name__
            view_definitions.extend(maker(log_db))
        
        print 'Syncing a total of %i views to CouchDB' % len(view_definitions)
        ViewDefinition.sync_many(log_db, view_definitions, remove_missing=True)
        
        print 'Finished'
        
    def sync_event_list_functions(self, event_db):
        """
        Synchronize list functions to the events database.
        """
        # Get path to dir containing list function definitions
        api_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        couchdb_dir = os.path.join(api_dir, 'couchdb')
        
        files = os.listdir(couchdb_dir)
        
        # Build dictionary of list functions
        list_funcs = {}
        
        for f in files:
            if re.match('.*_event_list.js', f):
                list_name = f[0:len(f)-14]
                abs_path = os.path.join(couchdb_dir, f)
                
                with open(abs_path, 'r') as f:
                    func = f.read()
                    
                list_funcs[list_name] = func
        
        print 'Syncing a total of %i list functions to CouchDB' % len(list_funcs)
        
        # Update the api design document 
        api_design_doc = event_db['_design/api']
        api_design_doc['lists'] = list_funcs
        event_db['_design/api'] = api_design_doc
        
        print 'Finished'

    
    def handle_noargs(self, **options):
        """
        Synchronize views defined in code to the CouchDB databases specified
        in settings.py.
        """
        server = couchdb.Server(settings.COUCHDB_SERVER_URI)
        event_db = server[settings.COUCHDB_EVENTDB_NAME]
        log_db = server[settings.COUCHDB_LOGDB_NAME]
        
        print 'Syncing event views...'
        self.sync_event_views(event_db)
        
        print 'Syncing log views...'
        self.sync_log_views(log_db)
        
        print 'Syncing event list functions...'
        self.sync_event_list_functions(event_db)
        
        print 'Exiting'