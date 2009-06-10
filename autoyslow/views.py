from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from yslow.autoyslow.models import Site, Page, Test
import spawnff
import datetime, time

def index(request):
	graphs = []
	tests = Test.objects.all()
	sites = {}
	for test in tests:
		try:
			sites[test.page.site][test.time].append(test.score)
		except KeyError:
			try:
				sites[test.page.site][test.time] = [test.score]
			except KeyError:
				sites[test.page.site] = {test.time: [test.score]}
	data = {}	
	for site in sites:
		for dtime in sites[site]:
			try:
				data[site].append([long(time.mktime(dtime.timetuple())*1000), (sum(sites[site][dtime]))/(len(sites[site][dtime]))]))
			except KeyError:
				data[site] = [[long(time.mktime(dtime.timetuple())*1000), (sum(sites[site][dtime]))/(len(sites[site][dtime]))]]	
	
	return render_to_response("index.html", {"graph_data": data})

def pages_index(request):
	page_list = Page.objects.all()
	return render_to_response("pages/index.html", {'page_list': page_list}) 

def page_detail(request, page_id):
	page = get_object_or_404(Page, id=page_id)
	return render_to_response("pages/detail.html", {'page': page}) 

def tests_index(request):
	return render_to_response("tests/index.html", {}) 

def run_test(request):
	try:
		url = request.POST['url']
	except KeyError:
		return render_to_response('tests/index.html', {
			'error_message': "You didn't put in a url.",
		})
	else:
		spawnff.run_test("/usr/bin/firefox", [url])
		return HttpResponseRedirect(reverse('yslow.autoyslow.views.tests_index'))

# idea for later: maybe have a dictionary with keys: api_id, value: function
def api(request, api_id=None):
	data = ""
	if api_id == "id":
		data = api_getbyid(request)
	elif api_id == "url":
		data = api_getbyurl(request)
	else:
		return HttpResponseRedirect(reverse('yslow.autoyslow.views.index'))
	return HttpResponse(data, mimetype="application/javascript")

def explore_api(request):
	data = api_getbyid(request)
	return render_to_response("api/api.html", {'data': data})

def api_getbyid(request):
	data = ""
	id = None
	try:
		id = request.POST['id']
	except KeyError:
		id = None

	if id == None:
		# TODO: get rid of string concatenation
		data = "["
		pages = Page.objects.all()
		for page in pages:
			location = '"location": "/api/pages/id/"'
			resource = '"resource": "%d"' % page.id
			data += "{%s, %s}," % (location, resource)
		data = data[0:len(data)-2] + "]"
	else:
		pages = [get_object_or_404(Page, pk=id)]
		data = serializers.serialize("json", pages)
	return data
	
def api_getbyurl(request):
	data = ""
	url = None
	try:
		url = request.POST['url']
	except KeyError:
		url = None	

	if url == None:
		data = "["
		inserted_urls = set()
		pages = Page.objects.all()
		for page in pages:
			if page.url not in inserted_urls:
				location = '"location": "/api/pages/url/"'
				resource = '"resource": "%s"' % page.url
				data += '{%s, %s}, ' % (location, resource)
				inserted_urls.add(page.url)
		data = data[0:len(data)-2] + "]"
	else:
		pages = Page.objects.filter(url=url)
		data = serializers.serialize("json", pages)
	return data 

def beacon(request):
	new_url = request.GET["u"]
	new_score = request.GET["o"]
	new_time = datetime.datetime.now()
	p = Page(url=new_url, overall_score=new_score, run_time=new_time)
	p.save()
	return HttpResponseRedirect(reverse('yslow.autoyslow.views.index')) 
