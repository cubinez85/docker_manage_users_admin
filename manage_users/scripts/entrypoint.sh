#!/bin/sh
# entrypoint.sh - Точка входа для Django-контейнера

set -e

echo "🚀 Starting Django application..."
echo "📋 DB_HOST=${DB_HOST:-db}, DB_PORT=${DB_PORT:-5432}"

# ✅ Проверка через Python socket (не требует psycopg2!)
wait_for_db() {
    echo "⏳ Waiting for PostgreSQL..."
    
    python3 << 'PYTHON_SCRIPT'
import socket
import os
import time

host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', 5432))
max_attempts = 60
attempt = 0

print(f"🔍 Trying to connect to {host}:{port}...")

while attempt < max_attempts:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ PostgreSQL is available!")
            exit(0)
    except Exception as e:
        pass
    
    attempt += 1
    print(f"⏳ Attempt {attempt}/{max_attempts} - PostgreSQL is unavailable, retrying in 2s...")
    time.sleep(2)

print("❌ Failed to connect to PostgreSQL after maximum attempts")
exit(1)
PYTHON_SCRIPT
}

# Ждём БД
wait_for_db

# Применяем миграции
echo "🔄 Applying migrations..."
python manage.py migrate --noinput

# Создаём суперпользователя
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "🔐 Checking superuser..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='${DJANGO_SUPERUSER_EMAIL:-}',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print(f"✅ Superuser '$DJANGO_SUPERUSER_USERNAME' created")
else:
    print(f"ℹ️  Superuser '$DJANGO_SUPERUSER_USERNAME' already exists")
EOF
fi

# Собираем статику
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Django initialization complete!"

# Запускаем Gunicorn
exec "$@"
