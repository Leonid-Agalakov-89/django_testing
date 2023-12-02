import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.usefixtures('bulk_create_news')
def test_news_count(admin_client):
    response = admin_client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('bulk_create_news')
def test_news_order(admin_client):
    response = admin_client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.usefixtures('create_comments')
def test_comments_order(admin_client, news_url, news):
    response = admin_client.get(news_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


def test_anonymous_client_has_no_form(admin_client, news_url):
    response = admin_client.get(news_url)
    assert 'form' in response.context


def test_authorized_client_has_form(author_client, news_url):
    response = author_client.get(news_url)
    assert 'form' in response.context
