"""
URL-конфигуратор приложения "Дневник".

Определяет все маршруты приложения дневника:
- Главная страница со списком записей
- Детальный просмотр записи
- Создание, редактирование и удаление записей
- Регистрация новых пользователей
"""

from django.urls import path

from . import views

app_name = "diary"

urlpatterns = [
    # Главная страница - список записей (включая поиск)
    path("", views.DiaryEntryListView.as_view(), name="entry_list"),
    # Детальный просмотр записи
    path("<int:pk>/", views.DiaryEntryDetailView.as_view(), name="entry_detail"),
    # Создание новой записи
    path("new/", views.DiaryEntryCreateView.as_view(), name="entry_create"),
    # Редактирование записи
    path("<int:pk>/edit/", views.DiaryEntryUpdateView.as_view(), name="entry_update"),
    # Удаление записи
    path("<int:pk>/delete/", views.DiaryEntryDeleteView.as_view(), name="entry_delete"),
    # Регистрация новых пользователей
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
