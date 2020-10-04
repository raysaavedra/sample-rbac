#!/bin/sh

echo "collect static"
python3 manage.py collectstatic --noinput
echo "migrate"
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000
