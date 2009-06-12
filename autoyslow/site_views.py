from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from cesium.autoyslow.models import Site, Page, Test, get_site_averages
import spawnff
import time
from datetime import datetime
import json
import itertools

def index(request):
    data = get_site_averages()
    
    # TODO: cookies
    # group into sites
    graphs_per_row = 3
    site_graphs = dict((id, list(it)) for (id, it) in itertools.groupby(data, lambda x: x['site_id']))
    
    # put dates in right format for JSON transfer
    json_data = dict()
    date_format = "%Y-%m-%d"
    for key in site_graphs.keys():
        json_data[key] = []
        for entry in site_graphs[key]:
            date_ms = time.mktime(datetime.strptime(entry['date'], date_format).timetuple())
            json_data[key].append([date_ms, entry['score']])
    json_data = json.dumps(json_data)

    # group each graph into rows
    rows = []
    for i in range(0, len(site_graphs.keys()), graphs_per_row):
        curr_row = []
        for key in site_graphs.keys()[i:i+graphs_per_row]:
            curr_row.append(site_graphs[key])
        rows.append(curr_row)
    
    # or if you prefer...
    # rows = [[site_graphs[key] for key in site_graphs.keys()[i:i+graphs_per_row]] for i in range(0, len(site_graphs.keys()), graphs_per_row)]
    return render_to_response("dashboard.html", {
        'data': data, 
        'json_data': json_data,
        'site_graphs': site_graphs,
        'rows': rows
    })

def pages_index(request):
    page_list = Page.objects.all()
    return render_to_response("pages/index.html", {'page_list': page_list}) 

def page_detail(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    return render_to_response("pages/detail.html", {'page': page}) 

def tests_index(request):
    return render_to_response("tests/index.html", {}) 
