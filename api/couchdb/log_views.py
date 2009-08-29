import couchdb
from couchdb.design import ViewDefinition

"""
This module defines a collection of functions which accept a CouchDB database
as an argument, are named with a 'make_views_*' convention, and return a list
of generated CouchDB ViewDefinitions.

The 'syncviews' management command dynamically executes each method to compile
a list of all Couchdb views.
"""
    
def make_views_all_documents(event_db):
    """
    Generate a view that includes all documents.
    """
    
    all_view_map_function = \
        '''
        function(doc) {
            emit(doc.access_datetime, doc)
        }
        '''
        
    return [ViewDefinition('api', 'all', all_view_map_function)]

def make_views_error_documents(event_db):
    """
    Generate a view that includes all documents.
    """
    
    error_view_map_function = \
        '''
        function(doc) {
            if (doc.result != "success") {
                emit(doc.access_datetime, doc)
            }
        }
        '''
        
    return [ViewDefinition('api', 'errors', error_view_map_function)]

def get_parser_list(event_db):
    """
    Return a list of unique parser names in the database.
    """
    
    parser_list_map_function = \
        '''
        function(doc) {
            emit(doc.parser_name, null);
        }
        '''
        
    parser_list_reduce_function = \
        '''
        function(keys, values) {
            return null;
        }
        '''
    
    return [
        e.key for e in event_db.query(
            parser_list_map_function,
            parser_list_reduce_function,
            group=True)]

def make_views_parser_lists(event_db):
    """
    Return a list of views, one for each parser, using templated view
    functions.
    """
    parser_names = get_parser_list(event_db)
    
    parser_view_map_function = \
        '''
        function(doc) {
            if (doc.parser_name == "%(parser_name)s") {
                emit(doc.parser_name, doc)
            }
        }
        '''
        
    return [
        ViewDefinition('api', name,
            parser_view_map_function % { 'parser_name': name })
        for name in parser_names]