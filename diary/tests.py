"""
Тесты для приложения "Дневник".
Проверяют основные функции модели, аутентификации и представлений.
"""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import DiaryEntry


class DiaryEntryModelTest(TestCase):
    """Тесты для модели DiaryEntry."""

    def setUp(self):
        """Настройка тестовых данных."""
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title="Тестовая запись",
            content="Содержимое тестовой записи",
        )

    def test_entry_creation(self):
        """Тест создания записи дневника."""
        self.assertEqual(self.entry.title, "Тестовая запись")
        self.assertEqual(self.entry.user.username, "testuser")
        self.assertTrue(self.entry.created_at)
        self.assertTrue(self.entry.updated_at)

    def test_entry_str_method(self):
        """Тест строкового представления записи."""
        self.assertEqual(str(self.entry), "Тестовая запись")

    def test_entry_get_absolute_url(self):
        """Тест получения абсолютного URL записи."""
        expected_url = reverse("diary:entry_detail", kwargs={"pk": self.entry.pk})
        self.assertEqual(self.entry.get_absolute_url(), expected_url)


class AuthenticationTest(TestCase):
    """Тесты аутентификации и регистрации."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123", email="test@example.com"
        )

    def test_registration_page_accessible(self):
        """Тест доступности страницы регистрации."""
        response = self.client.get(reverse("diary:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_successful_user_registration(self):
        """Тест успешной регистрации нового пользователя."""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "ComplexPassword123",
            "password2": "ComplexPassword123",
        }
        response = self.client.post(reverse("diary:register"), data)

        # Проверяем редирект после успешной регистрации
        self.assertEqual(response.status_code, 302)

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Проверяем, что новый пользователь автоматически вошел в систему
        user = User.objects.get(username="newuser")
        self.assertTrue(user.is_authenticated)

    def test_login_page_accessible(self):
        """Тест доступности страницы входа."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_successful_user_login(self):
        """Тест успешного входа пользователя."""
        login_successful = self.client.login(
            username="testuser", password="testpassword123"
        )
        self.assertTrue(login_successful)


class DiaryViewsTest(TestCase):
    """Тесты основных представлений дневника."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.entry = DiaryEntry.objects.create(
            user=self.user,
            title="Тестовая запись для просмотра",
            content="Содержимое тестовой записи для просмотра",
        )

    def test_entry_list_view_requires_login(self):
        """Тест: страница списка записей требует аутентификации."""
        response = self.client.get(reverse("diary:entry_list"))
        # Должен быть редирект на страницу входа (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_entry_list_view_authenticated(self):
        """Тест отображения списка записей для аутентифицированного пользователя."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("diary:entry_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diary/entry_list.html")
        self.assertContains(response, "Тестовая запись для просмотра")
        self.assertContains(response, "Мои записи")

    def test_entry_detail_view(self):
        """Тест детального просмотра записи."""
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("diary:entry_detail", args=[self.entry.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diary/entry_detail.html")
        self.assertContains(response, "Тестовая запись для просмотра")
        self.assertContains(response, "Содержимое тестовой записи для просмотра")

    def test_entry_create_view(self):
        """Тест создания новой записи дневника."""
        self.client.login(username="testuser", password="testpassword123")

        # Сначала проверяем, что форма доступна
        response = self.client.get(reverse("diary:entry_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diary/entry_form.html")

        # Тестируем отправку формы
        data = {
            "title": "Новая тестовая запись из теста",
            "content": "Содержимое новой записи созданной в тесте",
        }
        response = self.client.post(reverse("diary:entry_create"), data)

        # Проверяем редирект после успешного создания
        self.assertEqual(response.status_code, 302)

        # Проверяем, что запись создана
        self.assertTrue(
            DiaryEntry.objects.filter(
                title="Новая тестовая запись из теста", user=self.user
            ).exists()
        )


class AccessControlTest(TestCase):
    """Тесты контроля доступа к записям."""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # user1 создает запись
        self.entry = DiaryEntry.objects.create(
            user=self.user1,
            title="Приватная запись user1",
            content="Только user1 должен видеть эту запись",
        )

    def test_user_cannot_access_others_entry_detail(self):
        """Тест: пользователь не может просматривать чужие записи."""
        self.client.login(username="user2", password="password123")
        response = self.client.get(reverse("diary:entry_detail", args=[self.entry.pk]))

        # Должен получить 404, а не доступ к записи
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_access_others_entry_update(self):
        """Тест: пользователь не может редактировать чужие записи."""
        self.client.login(username="user2", password="password123")
        response = self.client.get(reverse("diary:entry_update", args=[self.entry.pk]))

        # Должен получить 404
        self.assertEqual(response.status_code, 404)
