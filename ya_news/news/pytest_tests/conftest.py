from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


def test_with_client(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def pk_for_args(news):  
    return news.pk,


@pytest.fixture
def form_data():
    return {
        'news': 'Новость',
        'author': 'Автор',
        'text': 'Текст комментария'
    }


@pytest.fixture
def new_form_data():
    return {'text': 'Обновлённый комментарий'}


@pytest.fixture
def news_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,)) 


@pytest.fixture
def bulk_create_news():
    today = datetime.today()
    return News.objects.bulk_create(
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=today - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )


@pytest.fixture
def create_comments(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comment
