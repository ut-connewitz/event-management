#!/bin/sh

sleep 60s

#celery -A events beat -l debug


mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

exec celery --app=events beat \
            -l debug \
            --loglevel=DEBUG --logfile=/var/log/celery/events.log \
            --uid=nobody --gid=nogroup
