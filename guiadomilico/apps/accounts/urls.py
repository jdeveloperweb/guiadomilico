from django.conf.urls import url
from guiadomilico.apps.accounts.views import views

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),

]
