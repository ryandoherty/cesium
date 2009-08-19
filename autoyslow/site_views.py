from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset 
from django.views.generic.create_update import create_object
from cesium.autoyslow.models import Site, Page, Test
import time
import datetime
from django.utils import simplejson
from django import forms
from forms import *

def index(request):
    return render_to_response("index.html", 
        {},
        context_instance=RequestContext(request)
    )

@login_required
def site_list(request):
    return render_to_response(
        "autoyslow/site_list.html",
        {'sites': request.user.get_profile().sites.all()},
        context_instance=RequestContext(request),
    )
        
@login_required
def site_detail(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    return render_to_response(
        "autoyslow/site_detail.html", 
        format_detail_dict(site, request.user),
        context_instance=RequestContext(request),
    ) 

@login_required
def page_detail(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    return render_to_response("autoyslow/page_detail.html", 
        format_detail_dict(page, request.user),
        context_instance=RequestContext(request)
    )

class JSONDatetimeEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            epoch_start = datetime.datetime.utcfromtimestamp(0)
            diff = o - epoch_start
            return (diff.days * 3600 + diff.seconds) * 1000
        elif isinstance(o, datetime.date):
            epoch_start = datetime.datetime.utcfromtimestamp(0)
            diff = (datetime.datetime.combine(o, datetime.time(0, 0, 0)) - 
                epoch_start)
            return (diff.days * 3600 + diff.seconds) * 1000
        return simplejson.JSONEncoder.default(self, o)

def format_detail_dict(obj, user):
    """Utility function for the Site and Page detail views"""
    header = obj.header(user)
    stats = obj.statistics(user)
    graph = obj.graph(user)
    return {
        'header': header,
        'header_json': simplejson.dumps(header, cls=JSONDatetimeEncoder),
        'statistics': stats,
        'statistics_json': simplejson.dumps(stats, cls=JSONDatetimeEncoder),
        'graph': graph,
        'graph_json': simplejson.dumps(graph, cls=JSONDatetimeEncoder)
    }

@login_required
def limited_password_reset(*args, **kwargs):
    return password_reset(*args, **kwargs)

@login_required
def add_site(request):
    if request.method == 'POST':
        redirect = create_object(
            request=request,
            login_required=True, 
            post_save_redirect='/',
            form_class=SiteForm
        )
        site = Site.objects.get(base_url=request.POST['base_url'])
        print site.id
        page = Page.objects.get_or_create(url='/', site=site)
        request.user.get_profile().pages.add(page)
        return redirect
   
    print "add_site GET" 
    return create_object(
        request,
        form_class=SiteForm,
        login_required=True
    )

@login_required
def remove_site(request, site_id):
    """If the Site is in the User's list of current Sites remove it.
        If the Site exists but is not in the User's list of Sites
        just return without doing anything. Otherwise return a 404 Not Found
    """
    site = get_object_or_404(Site, id=site_id)
    request.user.get_profile().sites.remove(site)
    return HttpResponseRedirect(
        reverse('cesium.autoyslow.site_views.index'))

@login_required
def update_user(request):
    if request.method == 'POST':
        f = UserForm(request.POST, instance=request.user)
        f.save()
        return HttpResponseRedirect(
            reverse('cesium.autoyslow.site_views.index'))

    return render_to_response(
        "auth/user_update_form.html",
        {'form': UserForm()},
        context_instance=RequestContext(request),
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',) 

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return HttpResponseRedirect(
            reverse('cesium.autoyslow.site_views.index'))
    
    return render_to_response(
        "auth/user_confirm_delete.html",
        context_instance=RequestContext(request),
    )

@login_required    
def add_page(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    profile = request.user.get_profile()
    # check to see if the specified Site is in the User's monitored Sites
    if site not in profile.sites.all():
        return HttpResponseRedirect(
            reverse('cesium.autoyslow.site_views.index'))
    
    page, created = Page.objects.get_or_create(
        url=request.POST['url'], site__id=site_id)
    request.user.get_profile().pages.add(page)
    return HttpResponseRedirect(
        reverse('cesium.autoyslow.site_views.index'))

@login_required
def remove_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    request.user.get_profile().pages.remove(page)
    return HttpResponseRedirect(
        reverse('cesium.autoyslow.site_views.index'))
