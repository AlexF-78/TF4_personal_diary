# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry и зависимости проекта
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

# Копируем остальной код проекта
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Запускаем Django сервер для разработки
# Используем 0.0.0.0 чтобы сервер был доступен снаружи контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
