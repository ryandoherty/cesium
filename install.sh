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
unzip install/firebug-1.3.3-fx.xpi -d install/firebug > /dev/null
EXT_PATH=`grep "em:id" install/firebug/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/firebug ${PROF_PATH}/extensions/${EXT_PATH}

echo "--> Installing YSlow..."
mkdir install/yslow
unzip install/yslow-2.0.0b4-fx.xpi -d install/yslow > /dev/null
EXT_PATH=`grep "em:id" install/yslow/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/yslow ${PROF_PATH}/extensions/${EXT_PATH}
