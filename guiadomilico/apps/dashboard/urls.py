from django.conf.urls import url
from . import views
from .views.views import DashboardView

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='index'),
    url(r'^posts$', views.views.post_list, name='posts'),
]
