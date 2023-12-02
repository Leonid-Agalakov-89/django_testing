from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_user_can_create_comment(author_client, author, form_data, news, news_url):
    url = news_url
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client, form_data, news_url):
    url = news_url
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    redirect_url = f'{login_url}?next={url}'
    assertRedirects(response, redirect_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(author_client, news_url):
        url = news_url
        bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
        response = author_client.post(url, data=bad_words_data)
        assertFormError(
            response,
            form='form',
            field='text',
            errors=WARNING
        )
        assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, delete_url, news_url):
        response = author_client.delete(delete_url)
        assertRedirects(response, f'{news_url}#comments')
        assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(admin_client, delete_url):
        response = admin_client.delete(delete_url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, comment, edit_url, new_form_data, news_url):
        response = author_client.post(edit_url, data=new_form_data)
        assertRedirects(response, f'{news_url}#comments')
        comment.refresh_from_db()
        assert comment.text == new_form_data['text']


def test_user_cant_edit_comment_of_another_user(admin_client, comment, edit_url, form_data):
    response = admin_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == form_data['text']