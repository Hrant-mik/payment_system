#!/bin/sh

mkdir -p /app/data
chmod 777 /app/data

python manage.py makemigrations
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"

python manage.py runserver 0.0.0.0:8000
