
from django.contrib.auth import logout, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.generic import FormView

from guiadomilico.apps.accounts.token import account_activation_token
from guiadomilico.apps.accounts.forms.cadastro import CadastroUserForm
from guiadomilico.apps.accounts.models.base import Usuario


class CadastroUserView(FormView):
    form_class = CadastroUserForm
    template_name = 'accounts/cadastro_usuario.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.is_trusty = False
        usuario.save()


        current_site = get_current_site(self.request)
        mail_subject = "[Guia do Milico] Ativação de usuário necessária"
        message = render_to_string('accounts/email_ativacao.html', {
            'usuario': usuario,
            'dominio': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
            'token': account_activation_token.make_token(usuario),
        })
        to_email = form.cleaned_data.get('email')

        email = EmailMessage(
            mail_subject,
            message,
            to=[to_email]
        )

        email.send()

        return super(CadastroUserView, self).form_valid(form)


def ativa(uidb64, token):
    _return = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None:
        if account_activation_token.check_token(user, token):
            user.is_trusty = True
            user.save()
        else:
            user = None
            _return['erro'] = 'Token inválido ou já utilizado!'
    else:
        _return['erro'] = 'Usuário inválido!'
    _return['usuario'] = user
    return _return


def ativarCadastro(request, uidb64, token):
    logout(request)

    _return = ativa(uidb64, token)
    if _return['usuario']:
        login(request, _return['usuario'])
        return redirect('core:index')
    else:
        context = {}
        context['erro'] = _return['erro']
        template_name = 'accounts/login.html'
        return render(request, template_name, context)