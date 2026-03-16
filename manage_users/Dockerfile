# syntax=docker/dockerfile:1.4

# === Stage 1: Build dependencies ===
FROM python:3.10-slim-bullseye AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt


# === Stage 2: Runtime image ===
FROM python:3.10-slim-bullseye AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN useradd -m -u 1000 -G www-data django_user

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=manage_users.settings

WORKDIR /app

# 🔥 1. Копируем весь проект
COPY --chown=django_user:www-data . /app/

# ✅ Гарантируем права на static и logs
RUN mkdir -p /app/static /app/logs && \
    chown -R django_user:django_user /app/static /app/logs

# Скрипт запуска
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# 🔥 2. Смена пользователя (после COPY!)
USER django_user

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/admin/ || exit 1

# 🔥 3. Копируем entrypoint.sh явно (после основного COPY!)
COPY --chown=django_user:www-data scripts/entrypoint.sh /entrypoint.sh

# 🔥 4. Делаем исполняемым
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "manage_users.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-"]
