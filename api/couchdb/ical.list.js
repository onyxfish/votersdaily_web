/* This CouchDB list function generates iCal for a given view. */
function(head, req) {
    // REMOVEME - Temprorary fix for un-normalized description fields
    String.prototype.normalize = function() {
        return this.replace(/^\\s+|\\s+$/g, '').replace(/\\s{2,}/g, ' ');
    };

    send('BEGIN:VCALENDAR\\n');
    send('VERSION:2.0\\n');
    send('PRODID:-//Voter\\'s Daily//NONSGML v1.0//EN\\n');

    var row;
    while(row = getRow()) {
        send('BEGIN:VEVENT\\n');
        
        var start = row.value.datetime.replace(/-/g, '').replace(/:/g, '');
        
        // Yes end date
        if (row.value.end_datetime) {
            var end = row.value.end_datetime.replace(/-/g, '').replace(/:/g, '');
            
            // All day event, multiple days
            if (start.substring(8) == 'T000000Z' && end.substring(8) == 'T000000Z')
            {
                send('DTSTART;VALUE=DATE:' + start.substring(0, 8) + '\\n');
                send('DTEND;VALUE=DATE:' + end.substring(0, 8) + '\\n');
            }
            // Normal event with end date
            else {
                send('DTSTART:' + start + '\\n');
                send('DTEND:' + end + '\\n');
            }
        }
        // No end date
        else {
            // Single day - all day event
            if (start.substring(8) == 'T000000Z')
            {
                send('DTSTART;VALUE=DATE:' + start.substring(0, 8) + '\\n');
            }
            // Normal event without end date
            else
            {
                send('DTSTART:' + start + '\\n');
            }
        }
        
        send('SUMMARY:' + row.value.title + '\\n');
        
        if (row.value.description) {
            send('DESCRIPTION:' + row.value.description.normalize() + '\\n');
        }
        
        send('URL:' + row.value.source_url + '\\n');
        send('CATEGORIES:' + row.value.branch + ',' + row.value.entity + '\\n');
        send('COMMENT:' + row.value.parser_name + ' ' + row.value.parser_version + '\\n');
    
        send('END:VEVENT\\n');
    }
    
    send('END:VCALENDAR');
}
