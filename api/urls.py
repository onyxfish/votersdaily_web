from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^events/all', 'votersdaily_web.api.views.events_all', name='api_events_all'),
    url(r'^events/branch/(?P<branch>.*)', 'votersdaily_web.api.views.events_branch', name='api_events_branch'),
    url(r'^events/entity/(?P<entity>.*)', 'votersdaily_web.api.views.events_entity', name='api_events_entity'),
)