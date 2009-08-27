import couchdb
from couchdb.design import ViewDefinition
from django.core.management.base import NoArgsCommand

from votersdaily_web import settings


class Command(NoArgsCommand):
    help = 'Synchronize views defined in the API to CouchDB.'
    
    def _init_couchdb(self):
        """
        Connect to CouchDB.
        """
        self.server = couchdb.Server(settings.COUCHDB_SERVER_URI)
        self.event_db = self.server[settings.COUCHDB_EVENTDB_NAME]
    
    def handle_noargs(self, **options):
        """
        Find all ViewDefinitions and sync them to the database
        """
        self._init_couchdb()
        
        print 'Importing view maker functions'
        
        # Import all view generator functions from the couchdb.views module
        from votersdaily_web.api.couchdb import views
        view_makers = [
            v for k, v in views.__dict__.items() if k.find('make_views') == 0]
        
        view_definitions = []
        
        for maker in view_makers:
            print 'Executing %s()' % maker.__name__
            view_definitions.extend(maker(self.event_db))
        
        print 'Syncing a total of %i views to CouchDB' % len(view_definitions)
        ViewDefinition.sync_many(
            self.event_db, view_definitions, remove_missing=True)
        
        print 'Finished'