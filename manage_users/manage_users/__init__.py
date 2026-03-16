"""
Package initialization for manage_users project.
"""

# Явная инициализация Django приложения (опционально для новых версий, но полезно)
import django
from django.conf import settings

# Проверка, что Django настроен перед использованием
if not settings.configured:
    pass  # Настройки загружаются через DJANGO_SETTINGS_MODULE

default_app_config = 'manage_users.apps.ManageUsersConfig'
