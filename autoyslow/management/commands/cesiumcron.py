import os
import sys
import atexit
from datetime import datetime, timedelta
import logging
from django.core.management.base import BaseCommand
from autoyslow.models import Site
from autoyslow import spawnff

def cleanup_pidfile(pidfile):
    os.unlink(pidfile)

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.setup_pid_file()
        
        print self.get_sites_to_test()
        
        # run tests
        for site in self.get_sites_to_test():
            spawnff.run_test(
                [(site.base_url+page.url) for page in site.page_set.all()])

    def setup_pid_file(self):
        pid = str(os.getpid())
        pidfile = os.path.expanduser('~/cesiumd.pid')
        if os.path.isfile(pidfile):
            logging.basicConfig(filename='logs/log.txt')
            logging.error(
                "%s exists - daemon is probably running - exiting..." % 
                pidfile
            )
            sys.exit()
        atexit.register(cleanup_pidfile, pidfile=pidfile)
        file(pidfile, 'w').write(pid)

    def get_sites_to_test(self):
        last_run_period = datetime.now() - timedelta(hours=24)
        return Site.objects.filter(userprofile__sites__gt=0).exclude(
            last_testrun__isnull=False, last_testrun__gt=last_run_period)
