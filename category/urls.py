from django.conf.urls import url

from home import views

urlpatterns = [


    url(r'^$', views.category, name='home'),
    url(r'^post/(?P<id>\d+)/$', views.post_single, name='post_single'),
    url(r'^post/addcomment/(?P<id>\d+)/$', views.addcomment, name='addcomment'),
    url(r'^add/$', views.post_new, name='post_new'),
    url(r'^post/(?P<id>.+)/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<id>.+)/$', views.post_delete, name='post_delete'),
]