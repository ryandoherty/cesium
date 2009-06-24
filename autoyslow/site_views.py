from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from cesium.autoyslow.models import Site, Page, Test, get_site_averages
import spawnff
import time
import datetime
import json
import itertools
from django import forms

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
            date_ms = time.mktime(datetime.datetime.strptime(entry['date'], date_format).timetuple())
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
    hours = range(1, 13)
    minutes = range(0, 60, 5)
    form = SiteForm(instance=site)
    return render_to_response("site_info.html", {
        'site': site,
        'hours': hours,
        'minutes': minutes,
        'form': form
    });

class SelectTimeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        hours = [[i, str(i)] for i in range(0, 24)]
        minutes = [[i, str(i)] for i in range(0, 60, 5)]
        minutes[0][1] = '00'
        minutes[1][1] = '05'
        widgets = (forms.widgets.Select(choices=hours),
                    forms.widgets.Select(choices=minutes))
        super(SelectTimeWidget, self).__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            return [value.hour, value.minute]
        return [None, None]

class SelectTimeField(forms.fields.MultiValueField):
    widget = SelectTimeWidget()
    def __init__(self, required=True, widget=None, label=None, initial=None):
        fields = (forms.fields.ChoiceField(),
                    forms.fields.ChoiceField())
        super(SelectTimeField, self).__init__(
            fields=fields, 
            widget=widget, 
            label=label, 
            initial=initial
        )

    def compress(self, data_list):
        if data_list:
            return datetime.time(
                hour=data_list[0], 
                minute=data_list[1], 
                second=0,
                microsecond=0
            )
        else:
            return None

class SiteForm(forms.ModelForm):
    test_time = SelectTimeField()    

    class Meta:
        model = Site
        exclude = ('base_url',)

def test_list(request):
    tests = get_upcoming_tests()
    return render_to_response("test_list.html", {
        'tests': tests
    });

def get_upcoming_tests():
    now = datetime.datetime.now()
    sites = [(time_til_next_test(site)+now, site) for site in Site.objects.all()]
    sites.sort()#cmp=lambda x, y: cmp(x[0], y[0]))
    return sites

def time_til_next_test(site):
    now = datetime.datetime.now()
    # hourly
    if site.freq == 'h':
        # if we've already done a test this hour...
        if now.minute > site.test_time.minute:
            return now.replace(hour=(now.hour+1), minute=site.test_time.minute) - now
        return now.replace(minute=site.test_time.minute) - now
    # daily 
    elif site.freq == 'd':
        # if we've already done a test today...
        if now.time().hour > site.test_time.hour or\
            (now.time().hour == site.test_time.hour and\
            now.time().minute > site.test_time.minute): 
            return now.replace(day=(now.day+1), hour=site.test_time.hour, minute=site.test_time.minute) - now
        return now.replace(hour=site.test_time.hour, minute=site.test_time.minute) - now
    # weekly
    elif site.freq == 'w':
        # if we've already done a test this week...
        # TODO: in desperate need of a heavily-scrutinizing code review...
        if (now.time().hour > site.test_time.hour and\
            now.date().weekday() == site.weekday) or\
            now.date().weekday() > site.weekday or\
            (now.time().hour == site.test_time.hour and\
            now.date().weekday() == site.weekday and\
            now.time().minute > site.test_time.minute):
            pass 
        return None
    else:
        raise ValueError, "Database corruption: value of freq not valid: " + site.freq

def update_site(request, site_id):
    s = Site.objects.get(id=site_id)
    test_time = datetime.time(
        hour=int(request.POST['test_time_0']),
        minute=int(request.POST['test_time_1']),
        second=0,
        microsecond=0
    )
    freq = request.POST['freq']
    weekday = request.POST['weekday']
    s.test_time, s.freq, s.weekday = test_time, freq, weekday
    s.save()
    s.save_schedule()
    return HttpResponseRedirect(reverse('cesium.autoyslow.site_views.site_info', args=(site_id,)))

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
