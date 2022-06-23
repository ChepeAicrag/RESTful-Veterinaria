#!/bin/bash

python manage.py migrate

# Apply site migrations
echo "Apply site migrations"
python manage.py loaddata users/fixtures/role.json

exec "$@"
