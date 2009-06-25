from django.db import models
from django.db import connection, transaction
import string
import os

class Site(models.Model):
    base_url = models.CharField(max_length=100)
    freq = models.CharField(max_length=1, choices=(
        ('h', 'Hourly'),
        ('d', 'Daily'),
        ('w', 'Weekly'),
    ))
    test_time = models.TimeField()
    weekday = models.SmallIntegerField(max_length=2, choices=(
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

    # cron files are of the format:
    # <minute> <hour> <day of month> <month> <day of week> /command
    def save_schedule(self):
        new_file = [] 
        if os.path.isfile('cesium.cron'):        
            cron_file = open('cesium.cron', 'r')
            line_dump = [string.rstrip(line) for line in cron_file]
            try:
                site_idx = line_dump.index("#"+self.base_url)
            except:
                site_idx = len(line_dump) 
            new_file = line_dump[0:site_idx]
            new_file.extend(line_dump[site_idx+2:])
            print new_file 
            cron_file.close()
        
        new_file.append("#"+self.base_url)
        command = "/home/mhahnenberg/Desktop/cesium/trunk/cesium/autoyslow/spawnff.py '/usr/bin/firefox' "
        for page in self.page_set.all():
            command += "'http://" + self.base_url + page.url + "'" + " "
        new_file.append(self.cron_time() + command + "\n")
        cron_file = open('cesium.cron', 'w')
        new_file = "\n".join(new_file)
        cron_file.write(new_file + "\n")
        cron_file.close()
        os.system("crontab -u root cesium.cron")

    # returns a properly formatted cron time string for this Site object
    def cron_time(self):
        if self.freq == 'h':
            cron_str = str(self.test_time.minute) + " * * * * "
        elif self.freq == 'd':
            cron_str = str(self.test_time.minute) + " " +\
                str(self.test_time.hour) + " * * * "
        elif self.freq == 'w':
            cron_str = str(self.test_time.minute) + " " +\
                str(self.test_time.hour) + " * * " +\
                str(self.weekday) + " "
        else:
            raise ValueError, "Database corruption: test_time data"
        return cron_str

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
    
