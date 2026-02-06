"""
Представления (Views) приложения "Дневник"

Содержит функции и классы для обработки HTTP-запросов и рендеринга страниц.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import DiaryEntryForm, SearchForm, UserRegisterForm
from .models import DiaryEntry


class DiaryEntryListView(LoginRequiredMixin, ListView):
    """
    Представление для списка всех записей пользователя.
        Наследует:
            model: Модель, записи которой отображаются
            template_name: Имя шаблона для рендеринга
            context_object_name: Имя переменной контекста в шаблоне
            paginate_by: Количество записей на странице
    """

    model = DiaryEntry
    template_name = "diary/entry_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        """
        Получение набора запросов (QuerySet) для отображения.
        Фильтрует записи по текущему пользователю и добавляет поиск.
        Returns:
            QuerySet: Отфильтрованные записи дневника
        """
        # Только записи текущего пользователя
        queryset = DiaryEntry.objects.filter(user=self.request.user)

        # Обработка поискового запроса
        search_form = SearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data["query"]:
            query = search_form.cleaned_data["query"]
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавление дополнительных данных в контекст шаблона.

        Args:
            **kwargs: Аргументы

        Returns:
            dict: Контекст шаблона с добавленной формой поиска
        """
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class DiaryEntryDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для детального просмотра записи дневника.

    Наследует:
        LoginRequiredMixin: Требует аутентификации пользователя
        DetailView: Базовый класс для отображения одного объекта
    """

    model = DiaryEntry
    template_name = "diary/entry_detail.html"
    context_object_name = "entry"

    def get_queryset(self):
        """
        Получение набора запросов с проверкой прав доступа.
        Пользователь может просматривать только свои записи.

        Returns:
            QuerySet: Записи текущего пользователя
        """
        return DiaryEntry.objects.filter(user=self.request.user)


class DiaryEntryCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой записи дневника.

    Наследует:
        LoginRequiredMixin: Требует аутентификации пользователя
        CreateView: Базовый класс для создания объектов
    """

    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "diary/entry_form.html"

    def form_valid(self, form):
        """
        Обработка валидной формы.
        Автоматически привязывает запись к текущему пользователю.

        Args:
            form: Валидная форма

        Returns:
            HttpResponse: Ответ после успешного сохранения
        """
        form.instance.user = self.request.user
        messages.success(self.request, "Запись успешно создана!")
        return super().form_valid(form)


class DiaryEntryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования существующей записи.

    Наследует:
        LoginRequiredMixin: Требует аутентификации пользователя
        UpdateView: Базовый класс для обновления объектов
    """

    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = "diary/entry_form.html"

    def get_queryset(self):
        """
        Получение набора запросов с проверкой прав доступа.
        Пользователь может редактировать только свои записи.

        Returns:
            QuerySet: Записи текущего пользователя
        """
        return DiaryEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Обработка валидной формы.

        Args:
            form: Валидная форма

        Returns:
            HttpResponse: Ответ после успешного обновления
        """
        messages.success(self.request, "Запись успешно обновлена!")
        return super().form_valid(form)


class DiaryEntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления записи дневника.

    Наследует:
        LoginRequiredMixin: Требует аутентификации пользователя
        DeleteView: Базовый класс для удаления объектов
    """

    model = DiaryEntry
    template_name = "diary/entry_confirm_delete.html"
    success_url = reverse_lazy("diary:entry_list")

    def get_queryset(self):
        """
        Получение набора запросов с проверкой прав доступа.
        Пользователь может удалять только свои записи.

        Returns:
            QuerySet: Записи текущего пользователя
        """
        return DiaryEntry.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        Обработка DELETE запроса.

        Args:
            request: HTTP запрос
            *args: Аргументы
            **kwargs: Ключевые аргументы

        Returns:
            HttpResponse: Ответ после удаления
        """
        messages.success(request, "Запись успешно удалена!")
        return super().delete(request, *args, **kwargs)


class UserRegisterView(CreateView):
    """
    Представление для регистрации новых пользователей.
    """

    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("diary:entry_list")

    def form_valid(self, form):
        """Автоматический вход после успешной регистрации."""
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
