#!/bin/bash

echo "=> Checking for container backend..."
if ! python manage.py ensurebackend; then
    exit 1
fi

# Start the first process
echo "=> Starting Worker"
python manage.py runworker docker




