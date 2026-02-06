"""
Модели приложения "Дневник".
Содержит модели для хранения записей дневника и связанных данных.
"""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class DiaryEntry(models.Model):
    """
    Модель для хранения записей дневника.

    Атрибуты:
        user (ForeignKey): Пользователь, создавший запись
        title (CharField): Заголовок записи (максимум 200 символов)
        content (TextField): Содержимое записи
        created_at (DateTimeField): Дата и время создания записи
        updated_at (DateTimeField): Дата и время последнего обновления

    Методы:
        __str__(): Возвращает заголовок записи
        get_absolute_url(): Возвращает URL для просмотра записи
        save(): Автоматически устанавливает created_at и updated_at
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="diary_entries",
        verbose_name="Пользователь",
    )

    title = models.CharField(max_length=200, verbose_name="Заголовок")

    content = models.TextField(verbose_name="Содержание")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        """
        Мета-класс для дополнительных настроек модели.

        Атрибуты:
            ordering: Сортировка записей по дате, новые сверху
            verbose_name: Человекочитаемое имя модели в единственном числе
            verbose_name_plural: Человекочитаемое имя модели во множественном числе
        """

        ordering = ["-created_at"]
        verbose_name = "Запись дневника"
        verbose_name_plural = "Записи дневника"

    def __str__(self):
        """
        Строковое представление записи.

        Returns:
            str: Заголовок записи
        """
        return self.title

    def get_absolute_url(self):
        """
        Получение абсолютного url для просмотра записи

        Returns:
            str: URL для просмотра записи
        """
        return reverse("diary:entry_detail", kwargs={"pk": self.pk})
