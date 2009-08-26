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
        
    def get_branch_list(self):
        """
        Return a list of unique branch names in the database.
        """
        
        branch_list_map_function = \
            '''
            function(doc) {
                emit(doc.branch, null);
            }
            '''
            
        branch_list_reduce_function = \
            '''
            function(keys, values) {
                return null;
            }
            '''
        
        return [
            e.key for e in self.event_db.query(
                branch_list_map_function,
                branch_list_reduce_function,
                group=True)]
        
    def generate_branch_views(self, branch_names):
        """
        Return a list of views, one for each branch, using templated view
        functions.
        """
        
        branch_view_map_function = \
            '''
            function(doc) {
                if (doc.branch == "%(branch_name)s") {
                    emit(doc.datetime, doc)
                }
            }
            '''
            
        return [
            ViewDefinition('api', name,
                branch_view_map_function % { 'branch_name': name })
            for name in branch_names]
        
    def get_entity_list(self):
        """
        Return a list of unique entity names in the database.
        """
        
        entity_list_map_function = \
            '''
            function(doc) {
                emit(doc.entity, null);
            }
            '''
            
        entity_list_reduce_function = \
            '''
            function(keys, values) {
                return null;
            }
            '''
        
        return [
            e.key for e in self.event_db.query(
                entity_list_map_function,
                entity_list_reduce_function,
                group=True)]
    
    def generate_entity_views(self, entity_names):
        """
        Return a list of views, one for each entity, using templated view
        functions.
        """
        
        entity_view_map_function = \
            '''
            function(doc) {
                if (doc.entity == "%(entity_name)s") {
                    emit(doc.datetime, doc)
                }
            }
            '''
            
        return [
            ViewDefinition('api', name,
                entity_view_map_function % { 'entity_name': name })
            for name in entity_names]
        
    def generate_all_view(self):
        
        all_view_map_function = \
            '''
            function(doc) {
                emit(doc.datetime, doc)
            }
            '''
            
        return ViewDefinition('api', 'all',all_view_map_function)
    
    def handle_noargs(self, **options):
        """
        Find all ViewDefinitions and sync them to the database
        """
        self._init_couchdb()
        
        print 'Generating branch views...'
        branch_names = self.get_branch_list()
        views = self.generate_branch_views(branch_names)
        
        print 'Generating entity views...'
        entity_names = self.get_entity_list()
        views.extend(self.generate_entity_views(entity_names))
        
        print 'Generating other (unique) views...'
        views.append(self.generate_all_view())
        
        print 'Syncing %i views to CouchDB...' % len(views)
        ViewDefinition.sync_many(
            self.event_db, views, remove_missing=True)
        
        print 'Finished.'