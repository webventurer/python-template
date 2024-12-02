#!/bin/bash
set -e

cores=$(nproc --all)
echo "Found [$cores] cores"
workers="$((cores*2+1))"
echo "Creating [$workers] workers"

gunicorn app1:__hug_wsgi__ \
    --workers=$workers \
    --bind 0.0.0.0:8000 \
    --log-level=info \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    --timeout 60 &

gunicorn app2:__hug_wsgi__ \
    --workers=$workers \
    --bind 0.0.0.0:8001 \
    --log-level=info \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    --timeout 60 &

sudo nginx -g 'daemon off;'

"$@"
