#!/bin/sh

BROWSER_PATH=/usr/bin/firefox

# create profile
${BROWSER_PATH} -CreateProfile "cesium"

# copy prefs to profile
cp install/user.js ${HOME}/.mozilla/firefox/*.cesium/user.js

# install add-ons
mkdir ${HOME}/.mozilla/firefox/*.cesium/extensions
mkdir install/firebug
unzip install/firebug-1.3.3-fx.xpi -d install/firebug
EXT_PATH=`grep "em:id" install/firebug/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/firebug ${HOME}/.mozilla/firefox/*.cesium/extensions/${EXT_PATH}


mkdir install/yslow
unzip install/yslow-2.0.0b4-fx.xpi -d install/yslow 
EXT_PATH=`grep "em:id" install/yslow/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv install/yslow ${HOME}/.mozilla/firefox/*.cesium/extensions/${EXT_PATH}
