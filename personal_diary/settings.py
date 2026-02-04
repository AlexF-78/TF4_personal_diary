"""
Конфигурация проекта "Личный дневник".

Этот файл содержит все настройки Django проекта, включая:
- Настройки безопасности
- Конфигурацию базы данных
- Пути к статическим файлам
- Установленные приложения
- Middleware
- Настройки шаблонов
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Ключ безопасности
SECRET_KEY = os.getenv("SECRET_KEY")
# Режим отладки
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = []


# Установленные приложения
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "diary",
]

# Middleware - Промежуточные слои обработки запросов
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Корневой URL конфигурации
ROOT_URLCONF = "personal_diary.urls"

# Конфигурация шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Глобальная папка шаблонов
        "APP_DIRS": True,  # Искать шаблоны в приложениях
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI приложение
WSGI_APPLICATION = "personal_diary.wsgi.application"


# Конфигурация базы данных
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Интернационализация
LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Статические файлы (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # Дополнительные папки со статикой
STATIC_ROOT = BASE_DIR / "staticfiles"  # Для collectstatic

# Медиа файлы (загруженные пользователями)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# URL для перенаправления после входа
LOGIN_REDIRECT_URL = "diary:entry_list"
LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Дефолтный primary key тип
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Для продакшн:
# DEBUG = False
# ALLOWED_HOSTS = ['ваш-домен.ru', 'localhost']
# CSRF_TRUSTED_ORIGINS = ['https://ваш-домен.ru']
