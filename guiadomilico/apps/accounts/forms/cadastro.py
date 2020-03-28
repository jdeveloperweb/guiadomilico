from django import forms
from django.contrib.auth.forms import UserCreationForm

from guiadomilico.apps.accounts.models.base import Usuario


class CadastroUserForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.EmailInput(),
        max_length=254,
        required=True
    )

    class Meta:
        model = Usuario
        fields = (
            'username',
            'email',
            'nome',
            'sobrenome',
            'password1',
            'password2'
        )