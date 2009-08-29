import random
import time
from datetime import datetime, timedelta
from operator import itemgetter

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from autoyslow.models import Page, Site, Test, User


class Command(BaseCommand):

    # (username, email, password) for passing to create_user
    users = [('test_account_1', 'test1@foo.com', 'user1password'),
             ('test_account_2', 'test2@foo.com', 'user2password'),
             ('test_account_3', 'test4@foo.com', 'user3password'),
            ]

    sites = ['google.com',
             'mozilla.com',
             'addons.mozilla.org',
             'microsoft.com',
            ]

    pages = ['/foo', '/bar', '/baz', '/something.html', '/page',
             '/login', '/logout', '/waytoolongpagename/that/should/truncate']

    @transaction.commit_on_success
    def handle(self, *args, **options):
        users = self.create_users()
        sites = self.create_sites(users)
        pages = self.create_pages(users, sites)
        self.create_tests(pages)

    def create_users(self):
        return [User.objects.create_user(*user) for user in self.users]

    def create_sites(self, users):
        new_sites = [Site.objects.create(base_url=url,
                                         last_testrun=datetime.now())
                     for url in self.sites]

        users[0].sites.add(*itemgetter(0,1,3)(new_sites))
        users[1].sites.add(new_sites[0])

        return new_sites

    def create_pages(self, users, sites):
        new_pages = [Page.objects.create(url=page, last_testrun=datetime.now(),
                                         site=sites[0])
                     for page in self.pages]

        users[0].pages.add(*itemgetter(0,1)(new_pages))
        users[1].pages.add(new_pages[2])

        return new_pages

    def create_tests(self, pages):
        for page in pages:
            for i in range(-60, 1):
                delta = timedelta(i)
                test_time = datetime.now() + delta
                new_test = Test(time=test_time, page=page,
                                score=random.randrange(40, 100, 1),
                                weight=random.randrange(200, 300, 1),
                                requests=random.randrange(10, 50, 1))
                new_test.save()
