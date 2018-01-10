from django.conf.urls import url

from home import views
from home.views import *

urlpatterns = [

    # url(r'^$', PostsListView.as_view(), name='list'),  # то есть по URL http://имя_сайта/blog/
    # будет выводиться список постов
    url(r'^$', home.as_view(), name='home'),
    url(r'^category/family/$', family.as_view(), name='family'),
    url(r'^category/health/$', health.as_view(), name='health'),
    url(r'^category/psychology/$', psychology.as_view(), name='psychology'),
    url(r'^post/(?P<id>\d+)/$', views.post_single, name='post_single'),
    url(r'^post/addcomment/(?P<id>\d+)/$', views.addcomment, name='addcomment'),
    url(r'^add/$', views.post_new, name='post_new'),
    url(r'^post/(?P<id>.+)/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<id>.+)/$', views.post_delete, name='post_delete'),
    url(r'^(?P<id>[0-9]+)/$', views.EPostView.as_view(), name='post'),
]
