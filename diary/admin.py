"""
Административная панель для приложения "Дневник".

Настройка интерфейса администратора для управления записями дневника.
"""

from django.contrib import admin

from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели DiaryEntry.

    Настройки:
        list_display: Поля, отображаемые в списке записей
        list_filter: Поля для фильтрации списка
        search_fields: Поля для поиска
        fieldsets: Группировка полей в форме редактирования
        readonly_fields: Поля только для чтения
    """

    list_display = ("title", "user", "created_at", "updated_at")
    list_filter = ("created_at", "user")
    search_fields = ("title", "content", "user__username")

    fieldsets = (
        ("Основная информация", {"fields": ("user", "title", "content")}),
        (
            "Метаданные",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_at", "updated_at")


# Настройка заголовка административной панели
admin.site.site_header = "Администрация Личного дневника"
admin.site.site_title = "Личный дневник"
admin.site.index_title = "Управление дневником"
