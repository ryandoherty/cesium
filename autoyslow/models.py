from django.db import models

class Site(models.Model):
	base_url = models.CharField(max_length=100)
	
class Page(models.Model):
	url = models.CharField(max_length=900)
	site = models.ForeignKey(Site)

	def __unicode__(self):
		return self.url

class Test(models.Model):
	score = models.IntegerField()
	time = models.DateTimeField('date tested')
	page = models.ForeignKey(Page)
	
