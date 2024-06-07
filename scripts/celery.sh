#!/bin/sh

celery -A events beat -l debug &
celery -A events worker -l info &
tail -f /dev/null
echo "*** celery initialisation done ***" ; \
