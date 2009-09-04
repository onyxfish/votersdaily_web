import json
import urllib2

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from votersdaily_web import settings


def all(request):
    """
    Renders a list of all documents.
    """
    if request.method != 'GET':
        raise Http404
    
    options = {}
    
    format = request.GET.get('format', 'json')
    
    try:
        options['endkey'] = request.GET['start']
    except KeyError:
        pass
    
    try:
        options['startkey'] = request.GET['startkey']
    except KeyError:
        pass
    
    options['descending'] = 'true'
    
    query_string = ''
    
    url = settings.API_ROOT + reverse('api_events_all') + query_string
    
    api_result = urllib2.urlopen(url)
    data = json.loads(api_result.read())
            
    return render_to_response('all.html', { 'documents': data['rows'] })

def branch(request, branch):
    """
    Renders a list of all documents.
    """
    print branch
    
    if request.method != 'GET':
        raise Http404
    
    options = {}
    
    format = request.GET.get('format', 'json')
    
    try:
        options['endkey'] = request.GET['start']
    except KeyError:
        pass
    
    try:
        options['startkey'] = request.GET['startkey']
    except KeyError:
        pass
    
    options['descending'] = 'true'
    
    query_string = ''
    
    url = settings.API_ROOT + reverse('api_events_branch', kwargs={'branch':branch}) + query_string
    
    api_result = urllib2.urlopen(url)
    data = json.loads(api_result.read())
                
    return render_to_response('branch.html', { 'documents': data['rows'] })
    