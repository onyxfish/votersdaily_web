from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^all', 'votersdaily_web.api.views.all', name='api_all'),
)