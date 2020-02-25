#! /usr/bin/env bash

set -e

python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin00@example.com', '${POSTGRES_PASSWORD}')" | python manage.py shell
python manage.py filldb
python manage.py runserver 0.0.0.0:8000
