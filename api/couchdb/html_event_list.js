/* This CouchDB list function generates simple HTML for a given view.
    This is mainly useful for debugging. */
function(head, req) {
    // REMOVEME - Temprorary fix for un-normalized description fields
    String.prototype.normalize = function() {
        return this.replace(/^\\s+|\\s+$/g, '').replace(/\\s{2,}/g, ' ');
    };

    send('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n');
    send('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n');
    
    send('\t<head>\n');
    send('\t\t<title>votersdaily quick html view</title>\n');
    send('\t</head>\n');
    
    send('\t<body>\n');
    send('\t\t<table border="1" margin="0" padding="0">\n');
    send('\t\t\t<tbody>\n');

    var row;
    while(row = getRow()) {
        send('\t\t\t\t<tr>');
        
        for (var i in row.value) {
        	if (!(i in {'_rev':1, 'source_text':1})) {
        		send('<td>' + row.value[i] + '</td>');
        	}
        }
    
        send('</tr>\n');
    }

    send('\t\t\t</tbody>\n');
    send('\t\t</table>\n');
    send('\t</body>\n');
    send('</html>');
}
