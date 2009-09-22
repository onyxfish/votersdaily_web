import datetime
import json
import urllib
import urllib2

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from votersdaily_web import settings


def get_query_options(request):
    """
    Parses query options common to all Citizen views from a request's GET dict.
    """
    options = {}
    
    try:
        options['start'] = request.GET['start']
    except KeyError:
        pass
    
    try:
        options['end'] = request.GET['end']
    except KeyError:
        pass
    
    options['format'] = 'json'
    
    return options

def all(request):
    """
    Renders a list of all events.
    """
    if request.method != 'GET':
        raise Http404
    
    api_url = settings.API_ROOT + reverse('api_events_all')
    
    options = get_query_options(request)
    query_string = urllib.urlencode(options)
    
    if query_string:
        api_url = '%s?%s' % (api_url, query_string)
    
    api_result = urllib2.urlopen(api_url)
    data = json.loads(api_result.read())
            
    return render_to_response('all.html', { 'documents': data['rows'] })

def branch(request, branch):
    """
    Renders a list of all events for a specific branch.
    """
    if request.method != 'GET':
        raise Http404
    
    api_url = settings.API_ROOT + reverse('api_events_branch', kwargs={'branch':branch})
    
    options = get_query_options(request)
    query_string = urllib.urlencode(options)
    
    if query_string:
        api_url = '%s?%s' % (api_url, query_string)
    
    api_result = urllib2.urlopen(api_url)
    data = json.loads(api_result.read())
                
    return render_to_response('branch.html', { 'documents': data['rows'] })

def entity(request, entity):
    """
    Renders a list of all events for a specific entity.
    """
    if request.method != 'GET':
        raise Http404
    
    api_url = settings.API_ROOT + reverse('api_events_entity', kwargs={'entity':entity})
    
    options = get_query_options(request)
    query_string = urllib.urlencode(options)
    
    if query_string:
        api_url = '%s?%s' % (api_url, query_string)
    
    api_result = urllib2.urlopen(api_url)
    data = json.loads(api_result.read())
                
    return render_to_response('entity.html', { 'documents': data['rows'] })

def index(request):
    """
    Renders the public-facing front page.
    """
    if request.method != 'GET':
        raise Http404
    
    utc_now = datetime.datetime.utcnow()
    utc_today = datetime.date(utc_now.year, utc_now.month, utc_now.day)
    utc_tomorrow = utc_today + datetime.timedelta(days=1)
    start = utc_today.isoformat()
    end = utc_tomorrow.isoformat()
    
    #TEMP
    start = '2009-09-01'
    end = '2009-09-15'
    
    options = {}
    options['start'] = start
    options['end'] = end
    options['format'] = 'json'
    query_string = urllib.urlencode(options)
    
    api_url = settings.API_ROOT + reverse('api_events_all')
    api_url = '%s?%s' % (api_url, query_string)
    
    api_result = urllib2.urlopen(api_url)
    data = json.loads(api_result.read())
    
    executive_events = []
    legislative_events = []
    judicial_events = []
    
    for key, value in data['results'].items():
        if value['branch'] == 'Executive':
            executive_events.append(value)
        elif value['branch'] == 'Legislative':
            legislative_events.append(value)
        elif value['branch'] == 'Judicial':
            judicial_events.append(value)
    
    return render_to_response('index.html', { 
        'executive_events': executive_events,
        'legislative_events': legislative_events,
        'judicial_events': judicial_events })
    