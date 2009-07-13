#!/bin/sh

BROWSER_PATH=/usr/bin/firefox

# create profile
${BROWSER_PATH} -CreateProfile "cesium"

# copy prefs to profile
cp user.js ${HOME}/.mozilla/firefox/*.cesium/user.js

# install add-ons
mkdir firebug
unzip firebug-1.3.3-fx.xpi -d firebug
EXT_PATH=`grep "em:id" firebug/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv firebug ${HOME}/.mozilla/firefox/*.cesium/extensions/${EXT_PATH}


mkdir yslow
unzip yslow-2.0.0b4-fx.xpi -d yslow 
EXT_PATH=`grep "em:id" yslow/install.rdf | grep "@" | cut -d">" -f2 | cut -d"<" -f1`
mv yslow ${HOME}/.mozilla/firefox/*.cesium/extensions/${EXT_PATH}
