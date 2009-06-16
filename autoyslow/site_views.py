from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from cesium.autoyslow.models import Site, Page, Test, get_site_averages
import spawnff
import time
from datetime import datetime, timedelta
import json
import itertools

def index(request):
    data = get_site_averages()
    
    # group into sites
    site_graphs = dict((id, list(it)) for (id, it) in itertools.groupby(data, lambda x: x['site_id']))
    
    # get any cookies...omnomnom
    try:
        comma = "%2C"
        site_order = request.COOKIES['graph_order'].split(comma)
    except KeyError:
        site_order = site_graphs.keys()

    sites = []
    for site_id in site_order:
        sites.append(site_graphs[int(site_id)])
    
    # put dates in right format for JSON transfer
    json_data = dict()
    date_format = "%Y-%m-%d"
    for key in site_graphs.keys():
        json_data[key] = []
        for entry in site_graphs[key]:
            date_ms = time.mktime(datetime.strptime(entry['date'], date_format).timetuple())
            json_data[key].append([date_ms, entry['score']])
    json_data = json.dumps(json_data)

    return render_to_response("dashboard.html", {
        'data': data, 
        'json_data': json_data,
        'site_graphs': site_graphs,
        'sites': sites
    })

def site_list(request):
    sites = Site.objects.all()
    return render_to_response("site_list.html", {
        'sites': sites
    });

def site_info(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    return render_to_response("site_info.html", {
        'site': site
    });

def test_list(request):
    now = datetime.now()
    oneday = timedelta(days=1)
    future = now + oneday
    tests = Test.objects.filter(time__range=(now, future))
    return render_to_response("test_list.html", {
        'tests': tests
    });

def add_page(request, site_id):
    url = request.POST['url']
    site = Site.objects.get(id=site_id)
    page = Page(url=url, site=site)
    page.save()
    return HttpResponseRedirect(reverse('cesium.autoyslow.site_views.site_info', args=(site.id,)))

def remove_page(request, site_id, page_id):
    site = Site.objects.get(id=site_id)
    page = Page.objects.get(id=page_id)
    page.delete()
    return HttpResponseRedirect(reverse('cesium.autoyslow.site_views.site_info', args=(site.id,)))
