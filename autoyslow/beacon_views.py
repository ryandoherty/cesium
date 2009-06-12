def beacon(request):
	new_url = request.GET["u"]
	new_score = request.GET["o"]
	new_time = datetime.datetime.now()
	p = Page(url=new_url, overall_score=new_score, run_time=new_time)
	p.save()
	return HttpResponseRedirect(reverse('yslow.autoyslow.views.index')) 
