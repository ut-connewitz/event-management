#!/bin/sh

echo "*** dockerfile script goind to sleep ***" ; \
sleep 60s &&
echo "*** beginning dockerfile script celery initialisation ***" ; \
celery -A events beat -l debug &&
celery -A events worker -l info &&
tail -f /dev/null
echo "*** celery initialisation done ***" ; \
