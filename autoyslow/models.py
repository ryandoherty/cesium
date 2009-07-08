from django.db import models
from django.db import connection, transaction
from datetime import datetime, timedelta
from django.conf import settings
import string

class Site(models.Model):
    base_url = models.CharField(max_length=100)
    freq = models.CharField(max_length=1, choices=(
        ('h', 'Hourly'),
        ('d', 'Daily'),
        ('w', 'Weekly'),
    ))
    test_time = models.TimeField()
    weekday = models.SmallIntegerField(choices=(
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ))

    def __unicode__(self):
        return self.base_url

    def next_test_time(self):
        now = datetime.now()
        return now + self.time_til_next_test(now)

    def time_til_next_test(self, now):
        days = hours = minutes = 0
        # weekly
        if self.freq == 'w':
            # if we've already done a test this week...
            if ((now.hour > self.test_time.hour and
                now.date().weekday() == self.weekday) or
                now.date().weekday() > self.weekday or
                (now.hour == self.test_time.hour and
                now.date().weekday() == self.weekday and
                now.minute > self.test_time.minute)):
                days = 6 - now.date().weekday() + self.weekday
            else:
                days = int(self.weekday) - now.date().weekday()
        # daily 
        if self.freq == 'w' or self.freq == 'd':
            # if we've already done a test today...
            if (now.hour > self.test_time.hour or
                (now.hour == self.test_time.hour and
                now.minute > self.test_time.minute)): 
                hours = 23 - now.hour + self.test_time.hour
            else:
                hours = self.test_time.hour - now.hour
        # hourly
        if self.freq == 'w' or self.freq == 'd' or self.freq == 'h':
            # if we've already done a test this hour...
            if now.minute > self.test_time.minute:
                minutes = 59 - now.minute + self.test_time.minute
            else:
                minutes = self.test_time.minute - now.minute
            return timedelta(days=days, hours=hours, minutes=minutes)
        else:
            raise (ValueError, 
                "Database corruption: invalid freq: %s" % self.freq)


# returns a list of dicts containing score, site_id, date, base_url keys
def get_site_averages():
    sql = """SELECT AVG(autoyslow_test.score), autoyslow_site.id,
    DATE(autoyslow_test.time),autoyslow_site.base_url FROM autoyslow_test 
    INNER JOIN autoyslow_page ON autoyslow_test.page_id=autoyslow_page.id 
    INNER JOIN autoyslow_site ON autoyslow_page.site_id=autoyslow_site.id 
    WHERE DATE(autoyslow_test.time)
    BETWEEN DATE_SUB(NOW(), INTERVAL '2' DAY) AND DATE(NOW())
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
   
    def __unicode__(self):
        return '(%s, %d)' % (self.time.ctime(), self.score)
