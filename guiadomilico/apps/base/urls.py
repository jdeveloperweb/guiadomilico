from django.conf.urls import url
from . import views


app_name = 'base'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]

#if DEBUG:
#    urlpatterns += [
#        url(r'^404/$', views.handler404),
#       url(r'^500/$', views.handler500),
#    ]