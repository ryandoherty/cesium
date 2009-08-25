from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.create_update import (
    create_object,
    update_object,
    delete_object
)
from autoyslow.site_views import limited_password_reset
from autoyslow.forms import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'cesium.autoyslow.site_views.index'),
    (r'^sites/$', 'cesium.autoyslow.site_views.site_list'),
    (r'^sites/(?P<site_id>\d+)/$', 
        'cesium.autoyslow.site_views.site_detail'),
    (r'^sites/new/$', 'cesium.autoyslow.site_views.add_site'),
    (r'^sites/remove/(?P<site_id>\d+)/$', 
        'cesium.autoyslow.site_views.remove_site'),
    (r'^pages/(?P<page_id>\d+)/$', 
        'cesium.autoyslow.site_views.page_detail'),
    (r'^pages/new/(?P<site_id>\d+)/$', 
        'cesium.autoyslow.site_views.add_page'),
    (r'^pages/remove/(?P<page_id>\d+)/$', 
        'cesium.autoyslow.site_views.remove_page'),
    
    # user authentication stuff
    (r'^accounts/new/$',
        create_object, 
        {'form_class': CesiumUserCreationForm, 'post_save_redirect': '/accounts/done',
        'template_name':'auth/user_new.html'},
        'accounts.new'
    ),
    (r'^accounts/done/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template': 'auth/user_new_done.html'}),
    (r'^accounts/update/$', 
        'cesium.autoyslow.site_views.update_user'),
    (r'^accounts/delete/$', 
        'cesium.autoyslow.site_views.delete_user'),
    (r'^accounts/delete/done/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template': 'auth/user_delete_done.html'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/reset/$', limited_password_reset),
    (r'^accounts/reset/done/$', 
        'django.contrib.auth.views.password_reset_done'),

    # admin interface stuff
    (r'^admin/(.*)', admin.site.root),
    
    # yslow beacon
    (r'^beacon/$', 'cesium.autoyslow.beacon_views.beacon'),
)

if settings.DEBUG:
   # Remove leading and trailing slashes so the regex matches.
   media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
   urlpatterns += patterns('',
      (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT})
      )
