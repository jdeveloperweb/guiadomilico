from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^loja-virtual/$', views.ShopView.as_view(), name='loja-virtual'),
    url(r'^sucesso/$', views.SucessView.as_view(), name='sucesso'),

]
