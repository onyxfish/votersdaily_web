import couchdb
from couchdb.design import ViewDefinition
from django.core.management.base import NoArgsCommand

from votersdaily_web import settings
from votersdaily_web.api import couchdb_views

class Command(NoArgsCommand):
    help = 'Synchronize views defined in the API to CouchDB.'
    
    def handle_noargs(self, **options):
        """
        Find all ViewDefinitions and sync them to the database
        """
        views = []
        
        for name in couchdb_views.__dict__:
            obj = getattr(couchdb_views, name)
            if isinstance(obj, ViewDefinition):
                views.append(obj)
        
        if views:
            server = couchdb.Server(settings.COUCHDB_SERVER_URI)
            event_db = server[settings.COUCHDB_EVENTDB_NAME]
            
            ViewDefinition.sync_many(event_db, views, remove_missing=True)