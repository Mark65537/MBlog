#!/bin/sh

echo "Waiting for database..."

# ждём БД (простейший вариант)
sleep 5

echo "Apply migrations"
python manage.py migrate

echo "Collect static"
python manage.py collectstatic --noinput

echo "Start server"
exec "$@"