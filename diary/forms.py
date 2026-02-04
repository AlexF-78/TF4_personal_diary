"""
Формы приложения "Дневник".
Содержит формы для создания дневника.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import DiaryEntry


class UserRegisterForm(UserCreationForm):
    """
    Форма для регистрации новых пользователей.
    Расширяет стандартную UserCreationForm.
    """

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш email"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Придумайте имя пользователя",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap к полям паролей
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Придумайте пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"}
        )
        # Добавляем help text
        self.fields["password1"].help_text = (
            "Пароль должен содержать минимум 8 символов"
        )
        self.fields["password2"].help_text = "Введите тот же пароль для подтверждения"


class DiaryEntryForm(forms.ModelForm):
    """
    Форма для создания и редактирования дневника.
    Наследуется от ModelForm для автоматического создания полей из модели.

    Атрибуты:
        Meta: Вложенный класс для настройки формы
    """

    class Meta:
        """
        Мета класс для настройки формы.
        Атрибуты:
            model: Модель на основе которой создаётся форма.
            fields: Поля модели, которые включаются в форму.
            widgets: Виджеты (Элементы управления) для моделей полей формы.
            labels: Подписи для полей формы.
        """

        model = DiaryEntry
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите заголовок записи",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Введите содержимое записи",
                }
            ),
        }
        labels = {
            "title": "Заголовок",
            "content": "Содержимое",
        }


class SearchForm(forms.Form):
    """
    Форма для поиска записей по заголовку и содержимому.
    Атрибуты:
        query (CharField): Поисковой запрос
    """

    query = forms.CharField(
        max_length=100,
        required=False,
        label="Поиск",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Поиск по заголовку или содержанию",
            }
        ),
    )
