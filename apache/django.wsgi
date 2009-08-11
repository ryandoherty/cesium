import os
import site
import sys

site.addsitedir('/a/cesium/virtual_env/lib/python2.6/site-packages/')
site.addsitedir('/a/cesium/trunk/')
site.addsitedir('/a/cesium/trunk/cesium/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'cesium.settings'
os.environ['PYTHON_EGG_CACHE']     = '/tmp/'

sys.stdout = sys.stderr

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
