#!/bin/sh

sleep 60s

#celery -A events beat -l debug


#mkdir -p /var/log/celery_beat
#chown -R nobody:nogroup /var/log/celery_beat

exec celery --app=events beat \
            -l debug \
            # --loglevel=DEBUG --logfile=/var/log/celery_beat/events.log \
            --uid=nobody --gid=nogroup
