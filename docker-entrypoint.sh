#!/bin/sh

set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Create First schema Fields..."
python manage.py create_dynamic_fields

echo "Create Initial Data ....."
python manage.py create_initial_data

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
