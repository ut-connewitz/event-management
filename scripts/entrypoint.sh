#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket :44444 --master --enable-threads --module events.wsgi
