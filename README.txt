Cesium 0.1

Note: This script is for installing versions of Cesium prior to 1.0.  If 
you are using Ubuntu, the installation instructions in this README are 
automated in the script "install.sh" in the main directory.  If you are 
trying to setup newer versions of Cesium (e.g. 1.0) on Red Hat Linux, 
there are instructions in "rhelsetup.txt".

The Python dependencies listed below will be installed inside a 
virtual environment using virtualenv if you choose to use virtualenv 
(which is recommended).  So you should REALLY know what you're doing if 
you choose to satisfy the dependencies without consulting the 
installation/configuration instructions which follow them.

Dependencies (again, read the install docs before charging ahead):

Firefox 3.0+ (as of 7/6/2009 YSlow is not compatible with Firefox 3.5.*)
Firebug 1.3.*
YSlow 2.0.0b4
Python 2.6
Django 1.0+
MySQL 5.0+
setuptools 0.6
mysql-python 1.2.3

Optional (but Recommended):
virtualenv 1.3.3

Preface:
All development was done primarily in an Ubuntu 9.04 virtual machine, so 
these things will probably work best there.  Broad-spectrum 
compatibility will be a feature for coming releases. 

Setup/Installation:

You will probably want to install Cesium inside a virtual machine or on 
some other computer since it will open and close Firefox repeatedly.

Check out the head revision of Cesium (0.1 at the time of this writing) 
at http://svn.mozilla.org/projects/cesium/trunk, which presumably 
you've already done ;-)

--Firefox Configuration:
Install the newest versions of the Firebug and YSlow Add-Ons in Firefox.
Firebug: https://addons.mozilla.org/en-US/firefox/addon/1843
YSlow: https://addons.mozilla.org/en-US/firefox/addon/5369

Edit /path/to/profile/user.js for the profile in which Firebug and YSlow are
installed with the following lines:

user_pref('extensions.yslow.beaconUrl', 
    'http://youripaddr:yourportnum/beacon');
user_pref('extensions.yslow.autorun', true);
user_pref('extensions.yslow.optinBeacon', true);
user_pref('browser.sessionstore.enabled', false);

--Django Configuration:

This setup method uses virtualenv so as not to mess with your global Python 
installation and potentially cause problems later down the road.  If you do
not want to use virtualenv just install the required packages using 
easy_install and hope for the best.  Most of the fixes regarding failures of
installation should apply to non-virtualenv installs as well.

Install MySQL if you haven't already and create a database named 'cesium' 
(sans quotes) in MySQL.

Create the appropriate users with the appropriate permissions 
(e.g. username='cesium, password='cesium') if you care enough or just use 
something you already have in there.


First install setuptools for Python by downloading the .egg file and 
following the instructions at http://pypi.python.org/pypi/setuptools

Next, run the following command to install virtualenv:

easy_install virtualenv

Note: you may have to run the previous command as root.  Create a new 
folder named virtual_env in /path/to/cesium/trunk/cesium.  Now create a 
fresh virtual environment for Python to run in with the following command:

virtualenv --no-site-packages /path/to/cesium/trunk/cesium/virtual_env

To load this virtual environment into the current shell, run the following 
commands:

cd /path/to/cesium/trunk/cesium/virtual_env
source bin/activate

Now you can install new Python packages without fear of screwing up your 
global Python install.  Any time you want to Cesium, you should first 
activate this virtual environment.  

You must install Django and mysql-python in this environment, which you 
can do with the following commands:

easy_install django
easy_install mysql-python

If the installation for mysql-python fails due to not being able to find 
"mysql_config" run the following command (on Ubuntu):

sudo apt-get install libmysqlclient15-dev
cd /path/to/cesium/trunk/cesium/virtual_env/build/mysql-python

Edit site.cfg in your editor of choice and uncomment the line:

#mysql_config=...

Replace the path in that file with the path to mysql_config on your 
computer, which is /usr/bin/mysql_config if you installed libmysqlclient on 
Ubuntu.  Save and exit the file.

If the installation fails because gcc cannot find Python.h, you don't have 
the development version of Python installed.  To remedy this, run the 
following command:

sudo apt-get install python-dev

After fixing any errors that occur, re-run the easy_install command to 
complete the installation of the required packages.

In /path/to/cesium/trunk/cesium, copy settings-dist.py as settings.py.  
Edit settings.py and change the database information so that it matches what
you just did in MySQL.  Also change all the relevant paths to wherever they 
are on your machine.  The list of variables that need changing if you used 
the suggested defaults is as follows:

MEDIA_ROOT (/path/to/cesium/trunk/cesium/media)
TEMPLATE_DIRS (/path/to/cesium/trunk/cesium/templates)

Run the following command in /path/to/cesium/trunk/cesium to create the 
proper tables in MySQL:

python manage.py syncdb

Note: this command will ask for some basic configuration information, just 
fill it out with whatever you want.

Start the development server in /path/to/cesium/trunk/cesium with:

python manage.py runserver youripaddr:yourportnum

Start the scheduling daemon in Python by entering these commands into the 
Python interpreter in /path/to/cesium/trunk/cesium:

from autoyslow import cesiumd
from django.conf import settings
cesiumd.CesiumDaemon(settings.AUTOYSLOW_DAEMON_PORT).start()

You can now access the web interface by navigating to 
http://youripaddr:yourportnum in a web browser.

Miscellaneous Notes:

Currently Django is setup in debug mode, which means that static content is 
served straight through Django's development server.  Check out their 
site for more information on that, but the main idea is that this is NOT 
appropriate for a production setting.
