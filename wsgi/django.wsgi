import os
import sys

sys.stdout = sys.stderr

sys.path.append('/var/www/bouvard.mashupkeyword.com/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'votersdaily_web.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
