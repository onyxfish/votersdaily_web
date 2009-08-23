import os
import sys

sys.stdout = sys.stderr

import django.core.handlers.wsgi

sys.path.append('/var/www/bouvard.mashupkeyword.com/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'votersdaily_web.settings'

application = django.core.handlers.wsgi.WSGIHandler()
