#!/bin/sh

sleep 60s

celery -A events beat -l debug
