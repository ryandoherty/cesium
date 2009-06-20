from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
	(r'^$', 'cesium.autoyslow.site_views.index'),
    (r'^sites/$', 'cesium.autoyslow.site_views.site_list'),
    (r'^sites/(?P<site_id>\d+)/$', 'cesium.autoyslow.site_views.site_info'),
    (r'^sites/(?P<site_id>\d+)/update/$', 'cesium.autoyslow.site_views.update_site'),
    (r'^sites/(?P<site_id>\d+)/pages/new/$', 'cesium.autoyslow.site_views.add_page'),
    (r'^sites/(?P<site_id>\d+)/pages/(?P<page_id>\d+)/remove/$', 'cesium.autoyslow.site_views.remove_page'),
    (r'^tests/$', 'cesium.autoyslow.site_views.test_list'),
    (r'^api/$', 'cesium.autoyslow.api_views.api'),
    (r'^beacon/$', 'cesium.autoyslow.beacon_views.beacon'),
)

if settings.DEBUG:
   urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': '/home/mhahnenberg/Desktop/cesium/trunk/cesium/media'})
      )
