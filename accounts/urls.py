# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from accounts.models import *
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^login/$', views.ELoginView.as_view(), name='login'),
    url(r'^article/(?P<pk>\d+)/bookmark/$',
        login_required(views.BookmarkView.as_view(model=BookmarkArticle)),
        name='article_bookmark'),
    url(r'^comment/(?P<pk>\d+)/bookmark/$',
        login_required(views.BookmarkView.as_view(model=BookmarkComment)),
        name='comment_bookmark'),
]