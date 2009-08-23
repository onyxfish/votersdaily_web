import json

import couchdb
from couchdb.design import ViewDefinition

view_all = ViewDefinition(
    'api', 'all', '''function(doc) { emit(doc._id, doc) }''');