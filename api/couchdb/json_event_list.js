/* This CouchDB list function generates simple JSON for a given view.
    This is to maintain consistency across backend changes. */
function(head, req) {
	// Documents will be collected in this object
	var docs = {};
	
	var row;
    while(row = getRow()) {
    	// Store id to be used as key
    	var id = row.value['_id'];
    	
    	for (var i in row.value) {
    		// Remove fields not useful to an end-user
	    	if (i in {'_id':1, '_rev':1, 'source_text':1}) {
	    		delete row.value[i];
	    	}
	    }
    	
    	// Add document to object
    	docs[id] = row.value;
    }
    
    // Hacker's pretty-printing
    var output = toJSON(docs);
    output = output.replace(/},/g, '},\n')
	
    // JSONify all collected documents
	send(output);
}
