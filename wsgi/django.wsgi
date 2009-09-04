import os
import sys

sys.stdout = sys.stderr

# Hack to get Django project on the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ['DJANGO_SETTINGS_MODULE'] = 'votersdaily_web.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
