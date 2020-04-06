from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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

'''
class UserChangeForm(UserChangeForm):
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
            'first_name',
            'last_name',
            'gender',
            'birthdate',
            'address',
            'city',
            'state',
            'CEP',
            'about',
            'site_facebook',
            'site_twitter',
            'profile_picture',
        )
'''