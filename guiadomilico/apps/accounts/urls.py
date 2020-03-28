from django.conf.urls import url
from django.urls import path

from guiadomilico.apps.accounts.views import login, cadastro

app_name = 'accounts'

urlpatterns = [
    url(r'login/$', login.LoginView.as_view(), name='login'),
    path('cadastro/', cadastro.CadastroUserView.as_view(), name='cadastroUsuario'),
    path('confirm/<str:uidb64>/<str:token>', cadastro.ativarCadastro, name='cadastroAtivar')

]
