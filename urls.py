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
    (r'^accounts/create/$', 
        create_object, 
        {'form_class': CesiumUserCreationForm}),
    (r'^accounts/update/(?P<object_id>\d+)/$',
        update_object, 
        {'form_class': CesiumUserUpdateForm, 'login_required': True}),
    (r'^accounts/delete/(?P<object_id>\d+)/$',
        delete_object, 
        {
            'model': User, 
            'post_delete_redirect': '/accounts/delete/done/', 
            'login_required': True
        }
    ),
    (r'^accounts/delete/done/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template': 'auth/user_delete_done.html'}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/reset/$', limited_password_reset),
    (r'^accounts/reset/done/$', 
        'django.contrib.auth.views.password_reset_done'),

    # admin interface stuff
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
   urlpatterns += patterns('',
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
         {'document_root': settings.MEDIA_ROOT})
      )
