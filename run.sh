#!/bin/bash

echo "=> Checking for container backend..."
if ! python manage.py ensurebackend; then
    exit 1
fi

echo "=> Waiting for DB to be online"
python manage.py wait_for_database -s 2

echo "=> Performing database migrations..."
python manage.py migrate

echo "=> Ensuring Superusers..."
python manage.py ensureadmin

echo "=> Collecting Static.."
python manage.py collectstatic --noinput
# Start the first process
echo "=> Starting Servers"
daphne -b 0.0.0.0 -p 80 port.asgi:application

