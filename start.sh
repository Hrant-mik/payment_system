#!/bin/sh

# Միգրացիաները իրականացնել
python manage.py makemigrations shop
python manage.py migrate

# Django server–ը լաունչ անել
python manage.py runserver 0.0.0.0:8000
