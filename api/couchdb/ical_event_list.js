/* This CouchDB list function generates iCal for a given view. */
function(head, req) {
    // REMOVEME - Temprorary fix for un-normalized description fields
    String.prototype.normalize = function() {
        return this.replace(/^\\s+|\\s+$/g, '').replace(/\\s{2,}/g, ' ');
    };
    
    send('BEGIN:VCALENDAR\r\\n');
    send('VERSION:2.0\r\n');
    send('PRODID:-//Voter\'s Daily//NONSGML v1.0//EN\r\n');

    var row;
    while(row = getRow()) {
        send('BEGIN:VEVENT\r\n');
        
        var start = row.value.datetime.replace(/-/g, '').replace(/:/g, '');
        
        // Yes end date
        if (row.value.end_datetime) {
            var end = row.value.end_datetime.replace(/-/g, '').replace(/:/g, '');
            
            // All day event, multiple days
            if (start.substring(8) == 'T000000Z' && end.substring(8) == 'T000000Z')
            {
                send('DTSTART;VALUE=DATE:' + start.substring(0, 8) + '\r\n');
                send('DTEND;VALUE=DATE:' + end.substring(0, 8) + '\r\n');
            }
            // Normal event with end date
            else {
                send('DTSTART:' + start + '\r\n');
                send('DTEND:' + end + '\r\n');
            }
        }
        // No end date
        else {
            // Single day - all day event
            if (start.substring(8) == 'T000000Z')
            {
                send('DTSTART;VALUE=DATE:' + start.substring(0, 8) + '\r\n');
            }
            // Normal event without end date
            else
            {
                send('DTSTART:' + start + '\r\n');
            }
        }
        
        send('SUMMARY:' + row.value.title + '\r\n');
        
        if (row.value.description) {
            send('DESCRIPTION:' + row.value.description.normalize() + '\r\n');
        }
        
        send('URL:' + row.value.source_url + '\r\n');
        send('CATEGORIES:' + row.value.branch + ',' + row.value.entity + '\r\n');
        send('COMMENT:' + row.value.parser_name + ' ' + row.value.parser_version + '\r\n');
    
        send('END:VEVENT\r\n');
    }
    
    send('END:VCALENDAR');
}
