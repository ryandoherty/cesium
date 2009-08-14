from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'cesium.autoyslow.site_views.index'),
    (r'^sites/(?P<site_id>\d+)/$', 
        'cesium.autoyslow.site_views.site_detail'),
    (r'^pages/(?P<page_id>\d+)/$', 
        'cesium.autoyslow.site_views.page_detail'),
    
    #(r'^sites/new/$', 'cesium.autoyslow.site_views.new_site'),
    #(r'^sites/new/add/$', 'cesium.autoyslow.site_views.add_site'),
    #(r'^sites/(?P<site_id>\d+)/remove/$', 
    #    'cesium.autoyslow.site_views.remove_site'),
    #(r'^sites/(?P<site_id>\d+)/data/$', 
    #    'cesium.autoyslow.site_views.site_data'),
    #(r'^sites/(?P<site_id>\d+)/pages/new/$', 
    #    'cesium.autoyslow.site_views.add_page'),
    #(r'^sites/(?P<site_id>\d+)/pages/(?P<page_id>\d+)/remove/$', 
    #    'cesium.autoyslow.site_views.remove_page'),
    #(r'^beacon/$', 'cesium.autoyslow.beacon_views.beacon'),
    
    # user authentication stuff
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

if settings.DEBUG:
   urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT})
      )
