from django.contrib.auth.forms import UserCreationForm

from guiadomilico.apps.accounts.models.base import Usuario


class CadastroUserForm(UserCreationForm):
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
