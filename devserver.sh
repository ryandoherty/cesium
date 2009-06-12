#!/bin/sh

# starts the development server on the specified network interface
if [ "${1}" != "" ]
then
    INTERFACE="${1}"
else
    INTERFACE="eth0"
fi

IFCONFIG_DUMP=`ifconfig`
CORRECT_INTERFACE=1
ADDR_LINE=1

for line in ${IFCONFIG_DUMP}
do
    if [ "${line}" = "${INTERFACE}" ]
    then
        CORRECT_INTERFACE=0
    fi
    IP_ADDR=`echo ${line} | grep -E "addr:([0-9]{1,3}\.){3}[0-9]{1,3}" | cut -d":" -f2`
    if [ ${CORRECT_INTERFACE} -a "${IP_ADDR}" != "" ]
    then
        python manage.py runserver ${IP_ADDR}:8000
        break
    fi
done
