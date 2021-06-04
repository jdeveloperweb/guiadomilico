from django.conf.urls import url
from .views import base

app_name = 'blog'
urlpatterns = [
    url(r'^$', base.post_list, name='list'),
    url(r'^post/(?P<pk>[0-9]+)/$', base.post_detail, name='detail'),
    url(r'^post/new/$', base.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', base.post_edit, name='post_edit'),
]