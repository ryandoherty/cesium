from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from cesium.autoyslow.models import Site, Page, Test
import datetime
from urlparse import urlparse

def beacon(request):
    parsed_url = urlparse(request.GET["u"])
    score = request.GET["o"]
    weight = request.GET["w"]
    requests = request.GET["r"]
    time = datetime.datetime.now()
    base_url = parsed_url.netloc
    url = parsed_url.path
    site = Site.objects.get(base_url=base_url)
    page = site.page_set.get(url=url, last_testrun=time)
    test = Test(
        score=score,
        weight=weight,
        requests=requests, 
        page=page, 
        time=time
    )
    test.save()
    return HttpResponseRedirect(
        reverse('cesium.autoyslow.site_views.index')) 
