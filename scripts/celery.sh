#!/bin/sh

sleep 60s

# celery -A events worker -l info


mkdir -p /var/run/celery /var/log/celery
chown -R nobody:nogroup /var/run/celery /var/log/celery

exec celery --app=events worker \
            --loglevel=INFO --logfile=/var/log/celery/events.log \
            --statedb=/var/run/celery/events@%h.state \
            --hostname=events@%h \
            --queues=celery.events -O fair \
            --uid=nobody --gid=nogroup
