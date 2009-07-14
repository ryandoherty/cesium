#!/bin/sh

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
sh install/setuptools-0.6c9-py2.6.egg

echo "--> Installing virtualenv..."
easy_install virtualenv

echo "--> Setting up virtual environment..."
virtualenv --no-site-packages virtual_env
echo "--> Running virtual environment..."
source virtual_env/bin/activate

echo "--> Installing pip..."
easy_install pip

echo "--> Installing pip requirements file..."
pip install -r install/dev-req.txt

echo "--> Done!"
