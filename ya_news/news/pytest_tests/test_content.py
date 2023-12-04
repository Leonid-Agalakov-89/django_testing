import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
@pytest.mark.usefixtures('bulk_create_news')
def test_news_count(admin_client, home_url):
    response = admin_client.get(home_url)
    news_catalog = response.context['object_list']
    news_count = len(news_catalog)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('bulk_create_news')
def test_news_order(admin_client, home_url):
    response = admin_client.get(home_url)
    news_list = response.context['object_list']
    all_dates = [news.date for news in news_list]
    assert [news.date for news in news_list
            ] == sorted(all_dates, reverse=True)


@pytest.mark.django_db
@pytest.mark.usefixtures('create_comments')
def test_comments_order(admin_client, news_url, news):
    response = admin_client.get(news_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    sorted_comments = sorted(all_comments, key=lambda x: x.created)
    assert sorted_comments == list(all_comments)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_url):
    response = client.get(news_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news_url):
    response = author_client.get(news_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
