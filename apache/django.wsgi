import os
import sys

sys.path.append('/usr/local/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'yslow.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
