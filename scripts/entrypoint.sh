#!/bin/sh

set -e

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser --noinput

python manage.py addbasedata

python manage.py addtestdata #remove for production deploy

uwsgi --socket :44444 --master --enable-threads --module events.wsgi
