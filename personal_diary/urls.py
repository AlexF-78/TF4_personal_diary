"""
Главный URL-конфигуратор проекта.

Определяет маршруты для всего проекта, включая маршруты приложений
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Админ-панель Django
    path("admin/", admin.site.urls),
    # URL приложения дневника
    path("", include("diary.urls")),
    # URL для аутентификации (используем встроенные представления Django)
    path("accounts/", include("django.contrib.auth.urls")),
]

# Маршруты для медиа-файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
