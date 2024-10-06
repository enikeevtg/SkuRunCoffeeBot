#!/bin/bash

weekday=$(date +'%a')
echo $weekday

if [ $weekday = 'Sat' ]; then
  make run
fi
