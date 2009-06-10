from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	 (r'^$', 'yslow.autoyslow.views.index'),
    (r'^api/$', 'yslow.autoyslow.views.api'),
    (r'^beacon/$', 'yslow.autoyslow.views.beacon'),
)

if settings.DEBUG:
   urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': '/usr/local/django/yslow/media'})
      )
