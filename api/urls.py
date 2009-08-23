from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^events/all', 'votersdaily_web.api.views.events_all', name='api_events_all'),
)