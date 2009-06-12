from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	 (r'^$', 'cesium.autoyslow.site_views.index'),
    (r'^api/$', 'cesium.autoyslow.api_views.api'),
    (r'^beacon/$', 'cesium.autoyslow.beacon_views.beacon'),
)

if settings.DEBUG:
   urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': '/home/mhahnenberg/Desktop/cesium/trunk/cesium/media'})
      )
