# this script "touches" the main wsgi application file for django, 
# thus getting the WSGI Daemon to update the models/views to the latest
# representation
touch -m /usr/local/django/yslow/apache/django.wsgi
