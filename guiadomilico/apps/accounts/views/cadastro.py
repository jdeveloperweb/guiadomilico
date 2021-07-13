from django.contrib.auth import logout, login

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView, TemplateView
from guiadomilico.apps.accounts.forms import EnderecoFormSet, TelefoneFormSet
from guiadomilico.apps.accounts.token import account_activation_token
from guiadomilico.apps.accounts.forms.cadastro import CadastroUserForm, CadastroUpdateForm
from guiadomilico.apps.accounts.models.base import Usuario, Endereco
from formtools.wizard.views import SessionWizardView
from  django.views.generic.edit import UpdateView
from  django.views.generic.list import ListView

import pycep_correios as pycep

from ..models import *

def send_mail(request, usuario):
    current_site = get_current_site(request)
    mail_subject = "[Guia do Milico] Ativação de usuário necessária"
    message = render_to_string('accounts/email_ativacao.html', {
        'usuario': usuario,
        'dominio': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
        'token': account_activation_token.make_token(usuario),
    })
    to_email = usuario.email

    email = EmailMessage(
        mail_subject,
        message,
        to=[to_email]
    )

    email.send()


## VIEW EM DESENVOLVIMENTO ##
class CadastroUpdateView(UpdateView):
    template_name = 'accounts/my_account.html'
    model = Usuario
    form_class = CadastroUpdateForm
    context_object_name = "usuario"

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse_lazy('accounts:my-account', kwargs={'pk': id })

    def get_context_data(self, **kwargs):
        id = self.kwargs.get(self.pk_url_kwarg)
        kwargs['usuario'] = Usuario.objects.filter(id=id).first()
        kwargs['usuario_form'] = CadastroUpdateForm(self.request.POST or None, instance=kwargs['usuario'])
        kwargs['endereco'] = list(Endereco.objects.filter(usuario_end__pk=self.kwargs['pk']).values())
        kwargs['TIPO_ENDERECO'] = TIPO_ENDERECO
        return super().get_context_data(**kwargs)



class CadastroListView(ListView):
    template_name = 'accounts/my_account.html'
    model = Usuario
    form_class = CadastroUserForm
    context_object_name = "usuario"


class EnderecoListView(ListView):
    template_name = 'accounts/my_account.html'
    model = Usuario
    form_class = CadastroUserForm
    context_object_name = "usuario"

class CadastroWizard(SessionWizardView):
    template_name = 'accounts/cadastro_usuario.html'

    FORMS = [("usuario", CadastroUserForm),
             ("endereco", EnderecoFormSet),
             ("telefone", TelefoneFormSet)
             ]

    form_list = FORMS


    def done(self, form_list, form_dict, **kwargs):

        template_name = 'accounts/email_notification.html'
        context = {}
        form_data = [form.cleaned_data for form in form_list]
        usuario = CadastroUserForm(form_data[0])
        user = usuario.save(commit=False)
        usuario.is_trusty = False
        instance = usuario.save()

        if 'endereco' in form_dict:
            formset = form_dict['endereco']
            if formset.is_valid():
                formset.instance = instance
                instance_endereco = formset.save()
                usuario.endereco_padrao = instance_endereco


        if 'telefone' in form_dict:
            formset = form_dict['telefone']
            if formset.is_valid():
                formset.instance = instance
                instance_telefone = formset.save()
                usuario.telefone_padrao = instance_telefone

        usuario.save()
        send_mail(self.request, user)

        # Context para avisar ao usuário que o cadastro foi efetuado com sucesso.
        # self.extra_context['form'] = self.get_form_instance(0)

        context['nomeCompleto'] = instance.get_full_name()
        context["emailEnvio"] = instance.email
        context["sucessoCadastro"] = "Um email foi enviado para {} com um link de ativação.".format(instance.email)

        return render(self.request, template_name, context )


'''
class CadastroUserView(FormView):
    form_class = CadastroUserForm
    template_name = 'accounts/cadastro_usuario.html'
    
    extra_context = {}
    endereco = EnderecoFormSet(prefix='endereco')
    telefone = TelefoneFormSet(prefix='telefone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["endereco"] = EnderecoFormSet(self.request.POST)
            context["telefone"] = TelefoneFormSet(self.request.POST)

        else:
            context["endereco"] = EnderecoFormSet()
            context["telefone"] = TelefoneFormSet()

        return context

    def get(self, request, *args, **kwargs):

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        endereco = EnderecoFormSet()
        telefone = TelefoneFormSet()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  endereco=endereco,
                                  telefone=telefone
                                  )
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        endereco = EnderecoFormSet(self.request.POST)
        telefone = TelefoneFormSet(self.request.POST)

        if form.is_valid() and endereco.is_valid():
            return self.form_valid(form, endereco, telefone)
        else:
            return self.form_invalid(form, endereco, telefone)

    def form_valid(self, form, endereco, telefone):
        usuario = form.save(commit=False)
        usuario.is_trusty = False
        self.object = form.save()
        endereco.instance = self.object
        endereco.save()
        telefone.instance = self.object
        telefone.save()
        send_mail(self.request, usuario)

        # Context para avisar ao usuário que o cadastro foi efetuado com sucesso.
        self.extra_context['form'] = self.form_class

        self.extra_context['nomeCompleto'] = "{} {}".format(usuario.nome, usuario.sobrenome)
        self.request.session["emailEnvio"] = usuario.email
        self.request.session["sucessoCadastro"] = "Um email foi enviado para {} com um link de ativação.".format(
            usuario.email)

        return super(CadastroUserView, self).form_valid(form)

    def form_invalid(self, form, endereco, telefone):

        return self.render_to_response(
            self.get_context_data(form=form,
                                  endereco=endereco,
                                  telefone=telefone
                                  )
        )

'''


def ativadoSucesso(request):
    template_name = 'accounts/active_sucess.html'
    return render(request, template_name)


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
        return redirect('accounts:ativado')
    else:
        context = {}
        context['erro'] = _return['erro']
        template_name = 'accounts/login.html'
        return render(request, template_name, context)


class EmailActiveView(TemplateView):
    template_name = 'accounts/email_notification.html'

    def get_context_data(self, **kwargs):
        context = super(EmailActiveView, self).get_context_data(**kwargs)
        context['sucessoCadastro'] = self.request.session["sucessoCadastro"]
        context['emailEnvio'] = self.request.session["emailEnvio"]
        del self.request.session["sucessoCadastro"]
        del self.request.session["emailEnvio"]

        return context


def accounts_inactive(request):
    logout(request)
    template_name = 'accounts/cadastro_inativo.html'
    context = {}

    if request.method == 'POST':
        username = request.POST['username']

        if Usuario.objects.filter(email=username).count() == 1:
            usuario = Usuario.objects.get(email=username)
        elif Usuario.objects.filter(username=username).count() == 1:
            usuario = Usuario.objects.get(username=username)
        else:
            usuario = None

        if usuario is not None:
            send_mail(request, usuario)

            request.session['sucessoCadastro'] = "Um email foi enviado para {} com um link de ativação.".format(
                usuario.email)
            request.session['emailEnvio'] = usuario.email

            return redirect(reverse('accounts:ativar-conta'))

        else:
            context['erro'] = "Nome de usuário/Email não encontrado!"

        return render(request, template_name, context)

    return render(request, template_name, context)


def is_exists_register_ajax(request):
    field = request.GET.get('field', None)
    validate = request.GET.get('validate', None)

    if validate is not None:
        if validate == 'username':
            is_tasken = Usuario.objects.filter(username__iexact=field).exists()
        elif validate == 'email':
            is_tasken = Usuario.objects.filter(email__iexact=field).exists()
        else:
            is_tasken = False;

    data = {
        'is_taken': is_tasken
    }
    return JsonResponse(data)


def validate_email_ajax(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': Usuario.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def consultar_cep(request):
    cep = request.GET.get('cep', None)
    endereco = pycep.get_address_from_cep(cep)
    endereco['validate'] = True

    return JsonResponse(endereco)
