#!/bin/bash

weekday=$(date +'%a')

if [ $weekday = 'Sat' ]; then
  echo "Запуск бота на pythonanywhere.com"
  python3 app/bot_pythonanywhere.py
else
  echo Today is $weekday
fi
