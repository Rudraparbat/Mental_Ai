#!/bin/sh

set -e  


echo "Starting Django server..."

python manage.py makemigrations
python manage.py migrate

daphne -b 0.0.0.0 -p 8000 mental.asgi:application


exec "$@"