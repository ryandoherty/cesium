from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from cesium.autoyslow.models import Site, Page, Test
import datetime
from urlparse import urlparse

def beacon(request):
    parsed_url = urlparse(request.GET["u"])
    new_score = request.GET["o"]
    new_time = datetime.datetime.now()
    base_url = parsed_url.netloc
    url = parsed_url.path
    site = Site.objects.get(base_url=base_url)
    page = site.page_set.get(url=url)
    test = Test(score=new_score, page=page, time=new_time)
    print "Test time: %s" % new_time.ctime()
    test.save()
    return HttpResponseRedirect(reverse('cesium.autoyslow.site_views.index')) 
