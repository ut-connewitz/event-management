#!/bin/sh

set -e

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

uwsgi --socket :44444 --master --enable-threads --module events.wsgi
