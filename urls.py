from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # WARNING: make sure to remove this for the production version
	 (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
	 	{'document_root': '/usr/local/django/yslow/media'}),
	 (r'^$', 'yslow.autoyslow.views.index'),
    (r'^pages/$', 'yslow.autoyslow.views.pages_index'),
    (r'^pages/(?P<page_id>\d+)/$', 'yslow.autoyslow.views.page_detail'),
    (r'^tests/$', 'yslow.autoyslow.views.tests_index'), 
    (r'^tests/run_test/$', 'yslow.autoyslow.views.run_test'),
    (r'^exploreapi/$', 'yslow.autoyslow.views.explore_api'),
    (r'^api/$', 'yslow.autoyslow.views.api'),
    (r'^api/pages/$', 'yslow.autoyslow.views.api'),
    (r'^api/pages/(?P<api_id>\w+)/$', 'yslow.autoyslow.views.api'),
    (r'^beacon/$', 'yslow.autoyslow.views.beacon'),
    # Example:
    # (r'^yslow/', include('yslow.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
