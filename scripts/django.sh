#!/bin/sh

mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

sleep 20s

python3 manage.py collectstatic --noinput &

# python3 manage.py migrate &

python3 manage.py runserver 0.0.0.0:8000
