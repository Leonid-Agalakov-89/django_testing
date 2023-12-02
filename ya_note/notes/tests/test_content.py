from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.author_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(title='Заголовок', text='Текст заметки', slug='note-slug', author=cls.author)

    def test_note_in_list_for_author(self):
        for name in ('notes:list',):
            with self.subTest(name=name):
                url = reverse(name)
                response = self.author_client.get(url)
                object_list = response.context['object_list']
                self.assertIn(self.note, object_list)


    def test_note_not_in_list_for_another_user(self):
        for name in ('notes:list',):
            with self.subTest(name=name):
                url = reverse(name)
                response = self.auth_client.get(url)
                object_list = response.context['object_list']
                self.assertIsNot(self.note, object_list)


    def test_pages_contains_form(self):
        for name, args in (
             ('notes:add', None),
             ('notes:edit', (self.note.slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
