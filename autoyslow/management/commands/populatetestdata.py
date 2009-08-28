from django.core.management.base import BaseCommand
from autoyslow.models import *
from django.contrib.auth.models import User
import time
import datetime
import random

class Command(BaseCommand):
    users = [{"username":"test_account_1", "email":"test1@foo.com", "password":"user1password"},
            {"username":"test_account_2", "email":"test2@foo.com", "password":"user2password"},
            {"username":"test_account_3", "email":"test4@foo.com", "password":"user3password"},]
    
    sites = [{"url":"google.com"},
            {"url":"mozilla.com"},
            {"url":"addons.mozilla.org"},
            {"url":"microsoft.com"},]
    
    pages = ["/foo", "/bar", "/baz", "/something.html", "/page", 
            "/login", "/logout", "/waytoolongpagename/that/should/truncate"]
    
    def handle(self, *args, **options):
        self.createUsers()
        self.createSites()
        self.createPages()
        self.createTests()
        
    def createUsers(self):
        for user in self.users:
            User.objects.create_user(user["username"], user["email"], user["password"])
    
    def createSites(self):
        new_sites = []
        for site in self.sites:
            new_site = Site(base_url=site["url"], last_testrun=datetime.datetime.now())
            new_site.save()
            new_sites.append(new_site)
        
        User.objects.get(username=self.users[0]["username"]).get_profile().sites.add(new_sites[0])
        User.objects.get(username=self.users[0]["username"]).get_profile().sites.add(new_sites[1])
        User.objects.get(username=self.users[1]["username"]).get_profile().sites.add(new_sites[0])
        User.objects.get(username=self.users[0]["username"]).get_profile().sites.add(new_sites[3])
        
    def createPages(self):
        new_pages = []
        
        for page in self.pages:
            new_page = Page(url=page, last_testrun=datetime.datetime.now())
            new_page.site = Site.objects.get(base_url=self.sites[0]["url"])
            new_page.save()
            new_pages.append(new_page)
            
        User.objects.get(username=self.users[0]["username"]).get_profile().pages.add(new_pages[0])
        User.objects.get(username=self.users[0]["username"]).get_profile().pages.add(new_pages[1])
        User.objects.get(username=self.users[1]["username"]).get_profile().pages.add(new_pages[2])
        User.objects.get(username=self.users[2]["username"]).get_profile().pages.add(new_pages[3])    
        
    def createTests(self):
        for page in self.pages:
            current_page = Page.objects.get(url=page)
            for i in range(-60, 1):
                timedelta = datetime.timedelta(i)
                test_time = datetime.datetime.now() + timedelta
                new_test = Test(time=test_time, score=random.randrange(40, 100, 1), 
                                weight=random.randrange(200, 300, 1), 
                                requests=random.randrange(10, 50, 1),)
                new_test.page = current_page
                new_test.save()