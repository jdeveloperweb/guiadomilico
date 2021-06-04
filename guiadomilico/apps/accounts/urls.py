from django.conf.urls import url
from django.urls import path

from guiadomilico.apps.accounts.views import login, cadastro

app_name = 'accounts'

urlpatterns = [
    url(r'login/$', login.LoginView.as_view(), name='login'),
    url(r'logout/$', login.LoginView.as_view(), name='logout'),
    path('cadastro/', cadastro.CadastroWizard.as_view(), name='cadastroUsuario'),
    path('my-account/', cadastro.UpdateUserView, name='my-account'),
    path('confirm/<str:uidb64>/<str:token>', cadastro.ativarCadastro, name='cadastroAtivar'),
    path('cadastro/ativar-conta', cadastro.EmailActiveView.as_view(), name='ativar-conta'),
    path('cadastro/reenviar-email', cadastro.accounts_inactive, name='cadastroReenvioEmail'),
    path('cadastro/ativado', cadastro.ativadoSucesso, name='ativado'),
    url('ajax/is_exists_register_ajax/', cadastro.is_exists_register_ajax, name='is_exists_register_ajax'),
    url('ajax/verifica_cep/', cadastro.consultar_cep, name='verifica_cep'),

]
