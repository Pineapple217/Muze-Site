#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

python manage.py runapscheduler &

gunicorn MuzeSite.wsgi:application --bind 0.0.0.0:8000 --log-file=-
