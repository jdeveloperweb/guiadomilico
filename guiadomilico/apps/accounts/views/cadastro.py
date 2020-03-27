from django.contrib.auth import login, logout
from django.core.validators import validate_email

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView

from django.shortcuts import render

from guiadomilico.apps.accounts.models.base import Usuario


class CadastroUserView(TemplateView):
    success_url = reverse_lazy('core:index')
    # form_class = CadastroUserForm
    template_name = 'accounts/cadastro_usuario.html'

