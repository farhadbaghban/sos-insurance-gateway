#!/bin/sh

set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Create First schema Fields..."
python manage.py create_dynamic_fields

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
