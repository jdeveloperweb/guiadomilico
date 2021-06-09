from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from guiadomilico.apps.accounts.models.base import Usuario, Endereco


class CadastroUserForm(UserCreationForm):



    email = forms.CharField(
        label="Endereço de E-mail",
        widget=forms.EmailInput(),
        max_length=254,
        required=True
    )


    class Meta:
        model = Usuario
        fields = (
            'nome',
            'sobrenome',
            'username',
            'email',
            'genero',
            'aniversario',
            'password1',
            'password2',
        )


        widgets = {
            'aniversario': forms.TextInput(attrs={'class': 'date'}),
        }



        labels = {
            'genero':'Genêro',
            'aniversario':'Data de nascimento',
        }

    def clean_aniversario(self):
            aniversario = self.cleaned_data['aniversario']

            if aniversario and aniversario >= date.today():
                raise forms.ValidationError('Digite uma data válida')

            return aniversario

   
        

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