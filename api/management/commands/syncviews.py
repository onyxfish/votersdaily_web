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
        
        print 'Exiting'