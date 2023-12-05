from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author
        )

    def test_pages_availability_for_anonymous_user(self):
        for name in (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        ):
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        for name in (
            'notes:list',
            'notes:success',
            'notes:add'
        ):
            with self.subTest(name=name):
                url = reverse(name)
                response = self.auth_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for user_client, status in users_statuses:
            for name in (
                'notes:detail',
                'notes:edit',
                'notes:delete'
            ):
                with self.subTest(user_client=user_client, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = user_client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        login_url = reverse('users:login')
        for name, args in (
                ('notes:list', None),
                ('notes:success', None),
                ('notes:add', None),
                ('notes:detail', (self.note.slug,)),
                ('notes:edit', (self.note.slug,)),
                ('notes:delete', (self.note.slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
