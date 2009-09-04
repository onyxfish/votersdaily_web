from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # API
    (r'^api/', include('votersdaily_web.api.urls')),
    
    # Citizen
    url(r'^all', 'votersdaily_web.citizen.views.all', name='all'),
    url(r'^branch/(?P<branch>.*)', 'votersdaily_web.citizen.views.branch', name='branch'),
)
