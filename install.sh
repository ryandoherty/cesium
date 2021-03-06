#!/bin/bash
#
#
# Note: This script works only on Ubuntu, and even then it is not guaranteed
#
#

BROWSER_PATH=/usr/bin/firefox

# create profile
echo "--> Creating new Firefox profile..."
${BROWSER_PATH} -CreateProfile "cesium"

# get random char string at front of profile folder name
CHAR_STR=`ls ${HOME}/.mozilla/firefox | grep "cesium" | cut -d"." -f1`
PROF_PATH=${HOME}/.mozilla/firefox/${CHAR_STR}.cesium

# copy prefs to profile
echo "--> Copying user preferences..."
cp install/user.js ${PROF_PATH}/user.js

# install add-ons
echo "--> Installing Firebug..."
mkdir ${PROF_PATH}/extensions
mkdir install/firebug
unzip -q install/firebug-1.3.3-fx.xpi -d install/firebug
EXT_PATH=`grep "em:id" install/firebug/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/firebug ${PROF_PATH}/extensions/${EXT_PATH}

echo "--> Installing YSlow..."
mkdir install/yslow
unzip -q install/yslow-2.0.0b4-fx.xpi -d install/yslow
EXT_PATH=`grep "em:id" install/yslow/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/yslow ${PROF_PATH}/extensions/${EXT_PATH}

# setup Python environment
echo "--> Installing setuptools..."
sudo sh install/setuptools-0.6c9-py2.6.egg

echo "--> Installing virtualenv..."
sudo easy_install -q virtualenv

echo "--> Setting up virtual environment..."
virtualenv --no-site-packages virtual_env
echo "--> Running virtual environment..."
source virtual_env/bin/activate

echo "--> Installing pip..."
easy_install -q pip

echo "--> Installing pip requirements file..."
pip install -q -r install/dev-req.txt

# setup other misc. things
echo "--> Copying settings..."
cp settings-dist.py settings.py
cp autoyslow/settings-dist.py autoyslow/settings.py

# register daemon
echo "--> Setting up scheduling daemon..."
# only works with update-rc.d currently
# TODO: make the path in cesiumd correct somehow
if [ `which update-rc.d` != "" ]
then
    sudo cp install/cesiumd /etc/init.d/cesiumd
    sudo update-rc.d cesiumd defaults
    sudo /etc/init.d/cesiumd start
fi

echo "--> Done!"
