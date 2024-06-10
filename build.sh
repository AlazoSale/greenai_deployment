#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static assets
python manage.py collectstatic --no-input

# Apply database migrations (optional)
python manage.py migrate

# Configure WSGI server (choose one based on your preference)

# Option 1: Gunicorn (recommended for production)
echo "Starting Gunicorn..."
gunicorn mysite.wsgi:application -b 0.0.0.0:$PORT