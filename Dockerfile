FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копируем код проекта
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000
