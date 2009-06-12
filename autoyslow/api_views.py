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
