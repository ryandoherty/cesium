from django.db import models
from django.contrib.auth.models import User

class Site(models.Model):
    base_url = models.CharField(max_length=100)
    last_testrun = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.base_url

    def __eq__(self, site):
        try:
            return self.base_url == site.base_url
        except AttributeError:
            return False

    def graph(self, user):
        """Return a dictionary of data for Site graphs.

        Current information included in dictionary:
        'score': the average of all ySlow scores for Pages of a Site by day
    
        Future information to include:
        'speed': average load time for Pages of a Site by day
        'size': average page size for Pages of a Site by day
        'requests': average number of requests for Pages of a Site by day
        """
        return {
            'score': [(date, avg_test_list(tests)) 
                for date, tests in self.group_tests_by_date(user).items()]
        }

    def group_tests_by_date(self, user):
        """Get data from Site in a dict like {date: [Test, ...], ...}"""
        dates = {}
        for page in self.get_pages_for_user(user):
            for test in page.test_set.all():
                dates.setdefault(test.time.date(), []).append(test)
        return dates

    def header(self, user):
        """Get basic info about the Site and return it in a dictionary.
    
        Current information included in dictionary:
        'score': the current average of ySlow scores for Pages on the Site
        'last_run': the datetime of the last testrun for this Site
        """
        header = {
            'score': self.avg_score(user), 
            'last_run': self.last_testrun 
        }
        return header
    
    def statistics(self, user):
        """Get stats about the Site and and return them in a dictionary.
        
        Current stats included in dictionary:
        'score': (with 'avg', 'best', and 'worst' details)
        """
        lastrun = self.last_testrun_tests(user)
        if lastrun:
            best = max(lastrun, key=lambda x: x.score).score
            worst = min(lastrun, key=lambda x: x.score).score
        else:
            best = worst = None

        stats = {
            'score': {
                        'avg': self.avg_score(user),
                        'best': best,
                        'worst': worst,
                    }
        }
        return stats
    
    def avg_score(self, user):
        """Get avg score of most recent Tests run on a Site for the User"""
        return avg_test_list(self.last_testrun_tests(user))
    
    def get_pages_for_user(self, user):
        """Get overlap of Pages for a Site and Pages that the User tracks"""
        return list(
            set(self.page_set.all()) & 
            set(user.get_profile().pages.filter(site__id=self.id))
        )
    
    def last_testrun_tests(self, user):
        """Get list of Tests from the last run of the Site for the User"""
        tests = []
        if self.last_testrun != None:
            for page in self.get_pages_for_user(user):
                tests.extend(page.test_set.filter(
                    time__gte=self.last_testrun)
                )
        return tests
    
class Page(models.Model):
    url = models.CharField(max_length=900)
    site = models.ForeignKey(Site)
    last_testrun = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.url

    def __eq__(self, page):
        try:
            return self.site == page.site and self.url == page.url
        except AttributeError:
            return False

    # user is not used, just exists to allow same function signature as Site
    def graph(self, user=None):
        """Create data of the format (date, score) and return in dict.
    
        Current information included in dictionary:
        'score': the ySlow score for the Page by day
        
        Future information to include:
        'speed': the load time for the Page of a Site by day
        'size': the page size for the Page of a Site by day
        'requests': the number of requests for the Page by day
        """
        return {
            # avg_test_list just in case we get more than one Test back
            'score': [(date, avg_test_list(tests)) 
                for date, tests in self.group_tests_by_date().items()]
        }
    
    def group_tests_by_date(self):
        """Get data from Page in a dict like {date: [Test, ...], ...}"""
        # TODO: make this able to narrow the date range
        dates = {}
        for test in self.test_set.all():
            dates.setdefault(test.time.date(), []).append(test)
        return dates
    
    # user is not used, just exists to allow same function signature as Site
    def header(self, user=None):
        """Get basic information about the Page and return it in a dict
    
        Current information included in dictionary:
        'score': the current ySlow score for this Page
        'last_run': the datetime of the last testrun for this Page
        """
        header = {
            'score': self.test_set.get(time=self.last_testrun).score,
            'last_run': self.last_testrun
        }
        return header
    
    def statistics(self, user):
        """Get statistics about the Page and and return them in a dict
        
        Current stats included in dictionary:
        'score': (with 'current', 'last', and 'site_avg' details).
        """
        tests = self.test_set.all().order_by('-time')
        current = tests[0].score if len(tests) > 0 else None
        last = tests[1].score if len(tests) > 1 else None
        stats = {
            'score': {
                        'current': current,
                        'last': last,
                        'site_avg': self.site.avg_score(user) 
                    }
        }
        return stats

class Test(models.Model):
    score = models.IntegerField()
    time = models.DateTimeField('date tested')
    page = models.ForeignKey(Page)
   
    def __unicode__(self):
        return '(%s, %d)' % (self.time.ctime(), self.score)

    def __eq__(self, test):
        try:
            return self.page == test.page and self.time == test.time
        except AttributeError:
            return False

def avg_test_list(tests):
    """Average the scores of a list of Tests and return the result"""
    if len(tests) == 0:
        return 0
    else:
        return (reduce(lambda x, y: x + y.score, tests, 0))/len(tests)

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    pages = models.ManyToManyField(Page)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.user.username
