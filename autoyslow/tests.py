from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from django.utils import simplejson

from autoyslow.models import Page, Site, Test, User
from autoyslow.site_views import JSONDatetimeEncoder, avg_test_list


class ModelsTestSuite(TestCase):
    fixtures = ['auth.json', 'autoyslow.json']

    def test_avg_test_list(self):
        self.assertEquals(avg_test_list(Test.objects.all()), 75)
        Test.objects.get(id=1).delete()
        self.assertEquals(avg_test_list(Test.objects.all()), 74)
        
    def test_site_avg(self):
        site = Site.objects.get(id=1)
        self.assertEquals(
            site.avg_score(User.objects.get(username='test')), 75
        )

    def test_get_last_testrun(self):
        expected = set(Test.objects.all())
        site = Site.objects.get(id=1)
        actual = set(site.last_testrun_tests(
            User.objects.get(username='test')))
        self.assertEquals(actual, expected)

    def test_get_pages_for_user(self):
        expected = set(Page.objects.all())
        site = Site.objects.get(id=1)
        actual = set(site.get_pages_for_user( 
            User.objects.get(username='test')))
        self.assertEquals(actual, expected)
        
        User.objects.get(username__exact='test').pages.remove(
            Page.objects.get(id=1))
        expected.remove(Page.objects.get(id=1))
        actual = set(site.get_pages_for_user( 
            User.objects.get(username='test')))
        self.assertEquals(actual, expected)

    def test_site_group_tests_by_date(self):
        site = Site.objects.get(id=1)
        actual = site.group_tests_by_date(
            User.objects.get(username='test')
        )
        expected = {site.last_testrun.date(): 
            list(Test.objects.all())}
        for key, value in actual.items():
            self.assertTrue(key in expected.keys())
            self.assertEquals(set(value), set(expected[key]))
        self.assertEquals(len(actual.keys()), len(expected.keys()))

    def test_page_group_tests_by_date(self):
        page = Page.objects.get(id=1)
        actual = page.group_tests_by_date()
        expected = {page.last_testrun.date(): 
            Test.objects.filter(page__id=page.id)}
        for key, value in actual.items():
            self.assertTrue(key in expected.keys())
            self.assertEquals(set(value), set(expected[key]))
        self.assertEquals(len(actual.keys()), len(expected.keys()))

    def test_site_header(self):
        site = Site.objects.get(id=1)
        actual = site.header(User.objects.get(username='test'))
        self.assertEquals(actual['score'], 75)
        self.assertEquals(actual['last_run'], site.last_testrun)
        self.assertEquals(len(actual.keys()), 2)

    def test_page_header(self):
        page = Page.objects.get(id=1)
        actual = page.header()
        self.assertEquals(actual['score'], 
            page.test_set.all().order_by('time')[0].score)
        self.assertEquals(actual['last_run'], 
            page.last_testrun)
        self.assertEquals(len(actual.keys()), 2)

    def test_site_statistics(self):
        site = Site.objects.get(id=1)
        actual = site.statistics(User.objects.get(username='test'))
        score = actual['score']
        self.assertEquals(score['avg'], 75)
        self.assertEquals(score['best'], 87)
        self.assertEquals(score['worst'], 59)
        self.assertEquals(len(actual.keys()), 1)
        self.assertEquals(len(score.keys()), 3)

    
    def test_site_statistics_empty_lastrun(self):
        for test in Test.objects.all():
            test.delete()
        site = Site.objects.get(id=1)
        user = User.objects.get(username="test")
        self.assertEquals(site.last_testrun_tests(user), [])
        actual = site.statistics(user)
        self.assertEquals(actual['score']['best'], None)
        self.assertEquals(actual['score']['worst'], None)

    def test_page_statistics(self):
        page = Page.objects.get(id=1)
        actual = page.statistics(User.objects.get(username='test'))
        score = actual['score']
        self.assertEquals(score['current'], 59)
        self.assertEquals(score['last'], 80)
        self.assertEquals(score['site_avg'], 75)
        self.assertEquals(len(actual.keys()), 1)
        self.assertEquals(len(score.keys()), 3)

    def test_page_statistics_no_tests(self):
        for test in Test.objects.all():
            test.delete()
        page = Page.objects.get(id=1)
        user = User.objects.get(username="test")
        self.assertEquals(len(page.test_set.all()), 0)
        actual = page.statistics(user)
        self.assertEquals(actual['score']['current'], None)
        self.assertEquals(actual['score']['last'], None)

    def test_site_graph(self):
        site = Site.objects.get(id=1)
        actual = site.graph(User.objects.get(username='test'))
        self.assertEquals(set(actual['score']), 
            set([(site.last_testrun.date(), 75)]))
        self.assertEquals(len(actual.keys()), 1)

    def test_page_graph(self):
        page = Page.objects.get(id=1)
        actual = page.graph()
        self.assertEquals(set(actual['score']), 
            set([(page.last_testrun.date(), 69)]))
        self.assertEquals(len(actual.keys()), 1)


class ViewsTestSuite(TestCase):
    fixtures = ['auth.json', 'autoyslow.json']
    
    def test_datetime_encoder(self):
        epoch_start = datetime.utcfromtimestamp(0)
        input = {"date1": epoch_start}
        expected = '{"date1": 0}'
        actual = simplejson.dumps(input, cls=JSONDatetimeEncoder)
        self.assertEquals(actual, expected)

class CommandsTestSuite(TestCase):
    fixtures = ['auth.json', 'autoyslow.json']
    
    def test_cesiumcron_get_sites(self):
        from autoyslow.management.commands.cesiumcron import Command
        # create a new site that hasn't been tested yet
        s = Site.objects.create(base_url='www.test.com')
        p = Page.objects.create(url='/', site=s)
        expected = set(Site.objects.all())
        actual = set(Command().get_sites_to_test())
        self.assertEquals(actual, expected)

        # add a test for the new site
        expected.remove(s)
        t = Test.objects.create(page=p, score=100, time=datetime.now())
        s.last_testrun = t.time
        s.save()
        actual = set(Command().get_sites_to_test())
        self.assertEquals(actual, expected)
        
