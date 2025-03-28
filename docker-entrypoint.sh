#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
# python manage.py runserver 0.0.0.0:8000
# gunicorn --bind 0.0.0.0:8000 --workers 8 --timeout 300 config.wsgi

echo "Starting server with custom Gunicorn configuration"
gunicorn --config python:gunicorn_config config.wsgi:application