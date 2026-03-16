"""
WSGI config for manage_users project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Указываем путь к файлу настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manage_users.settings')

# Создаем WSGI-приложение
application = get_wsgi_application()
