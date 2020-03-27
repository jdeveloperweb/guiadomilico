from django.conf.urls import url
from guiadomilico.apps.accounts.views import login, cadastro

app_name = 'accounts'

urlpatterns = [
    url(r'login/$', login.LoginView.as_view(), name='login'),
    url(r'^cadastro/$', cadastro.CadastroUserView.as_view(), name='cadastroUsuario'),

]
