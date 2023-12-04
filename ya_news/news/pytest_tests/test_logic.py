from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария'}
NEW_FORM_DATA = {'text': 'Обновлённый комментарий'}


def test_user_can_create_comment(
        author_client, author, news, news_url):
    count_comments = Comment.objects.count()
    response = author_client.post(news_url, data=FORM_DATA)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == count_comments + 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client, news_url, login_url):
    count_comments = Comment.objects.count()
    response = client.post(news_url, data=FORM_DATA)
    redirect_url = f'{login_url}?next={news_url}'
    assertRedirects(response, redirect_url)
    assert Comment.objects.count() == count_comments


def test_user_cant_use_bad_words(author_client, news_url):
    count_comments = Comment.objects.count()
    url = news_url
    bad_words_data = {
        'text': f'Какой-то текст, {choice(BAD_WORDS)}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == count_comments


def test_author_can_delete_comment(author_client, delete_url, news_url):
    count_comments = Comment.objects.count()
    response = author_client.delete(delete_url)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == count_comments - 1


def test_user_cant_delete_comment_of_another_user(admin_client, delete_url):
    count_comments = Comment.objects.count()
    response = admin_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count_comments


def test_author_can_edit_comment(
        author, author_client, comment, edit_url, news, news_url):
    response = author_client.post(edit_url, data=NEW_FORM_DATA)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
        author, admin_client, comment, edit_url, news):
    COMMENT_NOW = comment.text
    response = admin_client.post(edit_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_NOW
    assert comment.news == news
    assert comment.author == author
