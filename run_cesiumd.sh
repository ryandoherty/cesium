#!/bin/bash

cd $CESIUMPATH
$PYTHON manage.py cesiumcron >> logs/cronlog.txt
