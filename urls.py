from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # API
    (r'^api/', include('votersdaily_web.api.urls')),
    
    # Citizen
    url(r'^events/all', 'votersdaily_web.citizen.views.all', name='events_all'),
    url(r'^events/branch/(?P<branch>.*)', 'votersdaily_web.citizen.views.branch', name='events_branch'),
    url(r'^events/entity/(?P<entity>.*)', 'votersdaily_web.citizen.views.entity', name='events_entity'),
)
