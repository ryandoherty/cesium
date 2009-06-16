from django.db import models
from django.db import connection, transaction

class Site(models.Model):
    base_url = models.CharField(max_length=100)
    #hourly = models.BooleanField()
    #daily = models.BooleanField()
    #weekly = models.BooleanField()
    #test_time = models.TimeField()
    #weekday = models.CharField(max_length=2, choices=(
    #    ('M', 'Monday'),
    #    ('T', 'Tuesday'),
    #    ('W', 'Wednesday'),
    #    ('Th', 'Thursday'),
    #    ('F', 'Friday'),
    #    ('S', 'Saturday'),
    #    ('Su', 'Sunday')
    #))

# returns a list of dicts containing score, site_id, date, base_url keys
def get_site_averages():
    sql = """SELECT AVG(autoyslow_test.score), autoyslow_site.id,
    DATE(autoyslow_test.time),autoyslow_site.base_url FROM autoyslow_test 
    INNER JOIN autoyslow_page ON autoyslow_test.page_id=autoyslow_page.id 
    INNER JOIN autoyslow_site ON autoyslow_page.site_id=autoyslow_site.id 
    WHERE DATE(autoyslow_test.time)
    BETWEEN DATE('now', '-14 days') AND DATE('now')
    GROUP BY autoyslow_site.id, DATE(autoyslow_test.time)
    ORDER BY autoyslow_site.id"""

    cursor = connection.cursor()
    cursor.execute(sql)
    # order of labels is important -- it matches the order of the sql query
    labels = ['score', 'site_id', 'date', 'base_url']
    return [dict(zip(labels, row)) for row in cursor.fetchall()]
    
class Page(models.Model):
    url = models.CharField(max_length=900)
    site = models.ForeignKey(Site)

    def __unicode__(self):
        return self.url

class Test(models.Model):
    score = models.IntegerField()
    time = models.DateTimeField('date tested')
    page = models.ForeignKey(Page)
    
