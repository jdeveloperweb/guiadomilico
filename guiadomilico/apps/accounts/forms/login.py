from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe
from django.core.validators import validate_email

from guiadomilico.apps.accounts.models.base import Usuario

class LoginForm(AuthenticationForm):

    def confirm_login_permitido(self, user):
        if not user.is_trusty:
            raise forms.ValidationError(
                mark_safe(('Conta Inativa. <a href="#">Clique Aqui</a> para ativar'))
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            try:
                # Verifica se o valor digitado no campo login é um email válido, caso de erro, pula para o except
                validate_email(username)

                # Define o valor da variável username
                username = Usuario.objects.get(email=username).username
                self.user_cache = authenticate(self.request, username=username, password=password)

            except:
                # Define o valor da variável username para o username_field, pois deu erro na validação do email ou na authenticação
                username = username
                self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                try:
                    user_temp = Usuario.objects.get(username=username)
                except:
                    user_temp = None

                if user_temp is not None:
                    self.confirm_login_permitido(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name}
                    )

        return self.cleaned_data