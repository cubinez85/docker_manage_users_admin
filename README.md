# 👥 User Management API

Система управления пользователями на Django + Django Rest Framework с полной Docker-контейнеризацией.

## 🚀 Возможности

- ✅ CRUD операции с пользователями (создание, чтение, обновление, удаление)
- ✅ Ролевая модель доступа (RBAC)
- ✅ Фильтрация, поиск и пагинация
- ✅ Django Admin панель
- ✅ API документация (Swagger UI + Redoc)
- ✅ Basic Auth через Nginx
- ✅ Полная Docker-контейнеризация (Django + PostgreSQL + Nginx)
- ✅ Готово к продакшену

## 📋 Требования

- Docker 24.0+
- Docker Compose 2.20+
- Git

## 🛠️ Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/cubinez85/manage_users.git
cd manage_users

Запуск проекта:
# Сборка и запуск всех сервисов
docker compose up --build -d

# Проверка статуса
docker compose ps

# Просмотр логов
docker compose logs -f

Docker Compose:
# Запуск
docker compose up -d

# Остановка
docker compose down

# Перезапуск
docker compose restart

# Просмотр логов
docker compose logs -f

# Выполнить команду в контейнере
docker compose exec django python manage.py migrate

Тесты:
docker compose exec django python manage.py test

Развёртывание на другом сервере (без сборки!):
На новом сервере:
# 1. Установите Docker (если нет)
curl -fsSL https://get.docker.com | sh

# 2. Создайте директорию проекта
mkdir -p /var/www/manage_users
cd /var/www/manage_users

# 3. Скопируйте файлы конфигурации
# (docker-compose.prod.yml, .env, nginx/nginx.conf, nginx/.htpasswd)

# 4. Запустите проект (образы скачаются из Docker Hub)
docker compose -f docker-compose.prod.yml up -d

# 5. Проверьте статус
docker compose ps
