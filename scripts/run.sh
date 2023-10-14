#!/bin/sh

set -e

python manage.py wait_for_db_ready
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module buffetiser.wsgi