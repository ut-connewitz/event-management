#!/bin/sh

sleep 60s

celery -A events worker -l info
