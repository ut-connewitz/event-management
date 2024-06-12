#!/bin/sh

python3 manage.py runserver 0.0.0.0:8000 &

python3 manage.py collectstatic &

python3 manage.py migrate &

sleep 60s

celery -A events beat -l debug &

celery -A events worker -l info
