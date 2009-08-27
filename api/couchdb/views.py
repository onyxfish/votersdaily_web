import couchdb
from couchdb.design import ViewDefinition

"""
This module defines a collection of functions which accept a CouchDB database
as an argument, are named with a 'make_views_*' convention, and return a list
of generated CouchDB ViewDefinitions.

The 'syncviews' management command dynamically executes each method to compile
a list of all Couchdb views.
"""

def get_branch_list(event_db):
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
        e.key for e in event_db.query(
            branch_list_map_function,
            branch_list_reduce_function,
            group=True)]
    
def make_views_branch_lists(event_db):
    """
    Return a list of views, one for each branch, using templated view
    functions.
    """
    branch_names = get_branch_list(event_db)
    
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
    
def get_entity_list(event_db):
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
        e.key for e in event_db.query(
            entity_list_map_function,
            entity_list_reduce_function,
            group=True)]

def make_views_entity_lists(event_db):
    """
    Return a list of views, one for each entity, using templated view
    functions.
    """
    entity_names = get_entity_list(event_db)
    
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
    
def make_views_all_documents(event_db):
    """
    Generate a view that includes all documents.
    """
    
    all_view_map_function = \
        '''
        function(doc) {
            emit(doc.datetime, doc)
        }
        '''
        
    return [ViewDefinition('api', 'all', all_view_map_function)]