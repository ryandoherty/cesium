from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from cesium.autoyslow.models import Site, Page, Test
import time
import datetime
from django.utils import simplejson
from django import forms

def index(request):
    return render_to_response("index.html", 
        {},
        context_instance=RequestContext(request)
    )
        
@login_required
def site_detail(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    return render_to_response("autoyslow/site_detail.html", 
        format_detail_dict(site, request.user),
        context_instance=RequestContext(request)
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

def new_site(request):
    form = SiteForm()
    return render_to_response(
        "site_info.html", 
        {'form': form},
        context_instance=RequestContext(request)
    );
    
def add_site(request):
    s = Site(base_url=request.POST['base_url'])
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
    save_schedule(s)
    return HttpResponseRedirect(reverse('cesium.autoyslow.site_views.site_info', args=(s.id,)))
    
def remove_site(request, site_id):
    s = Site.objects.get(id=site_id)
    s.delete()
    return HttpResponseRedirect(
        reverse('cesium.autoyslow.site_views.site_list'))

def site_info(request, site_id=None):
    site = get_object_or_404(Site, pk=site_id)
    hours = range(1, 13)
    minutes = range(0, 60, 5)
    form = SiteForm(instance=site)
    return render_to_response("site_info.html", 
        {
            'site': site,
            'hours': hours,
            'minutes': minutes,
            'form': form
        },
        context_instance=RequestContext(request)
    )

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

def site_data(request, site_id):
    site = Site.objects.get(id=site_id)
    id_name_dict = dict((page.id, page.url) for page in site.page_set.all())
    page_graphs = dict((page.id, [(time.mktime(test.time.timetuple()), test.score) for test in page.test_set.all()]) for page in site.page_set.all())
    
    return render_to_response('site_data.html', 
        {
            'site': site,
            'pages': page_graphs,
            'id_name_dict': id_name_dict,
            'json_data': simplejson.dumps(page_graphs)
        },
        context_instance=RequestContext(request)
    )
