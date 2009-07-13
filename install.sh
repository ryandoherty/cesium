#!/bin/sh

BROWSER_PATH=/usr/bin/firefox

# create profile
${BROWSER_PATH} -CreateProfile "cesium"

# get random char string at front of profile folder name
CHAR_STR=`ls ${HOME}/.mozilla/firefox | grep "cesium" | cut -d"." -f1`
PROF_PATH=${HOME}/.mozilla/firefox/${CHAR_STR}.cesium

# copy prefs to profile
cp install/user.js ${PROF_PATH}/user.js

# install add-ons
mkdir ${PROF_PATH}/extensions
mkdir install/firebug
unzip install/firebug-1.3.3-fx.xpi -d install/firebug
EXT_PATH=`grep "em:id" install/firebug/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/firebug ${PROF_PATH}/extensions/${EXT_PATH}


mkdir install/yslow
unzip install/yslow-2.0.0b4-fx.xpi -d install/yslow 
EXT_PATH=`grep "em:id" install/yslow/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/yslow ${PROF_PATH}/extensions/${EXT_PATH}
