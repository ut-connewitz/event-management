#!/bin/sh

set -e

python3 manage.py collectstatic --noinput &

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py addbasedata &

python3 manage.py runserver 0.0.0.0:8000

uwsgi --socket :8000 --master --enable-threads --module app.wsgi
