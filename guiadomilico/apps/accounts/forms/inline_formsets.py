# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from guiadomilico.apps.accounts.models import Telefone, Endereco, Usuario


class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = (
            'tipo_telefone',
            'telefone',
        )

        labels = {
            'telefone':'DDD + Telefone',
            'tipo_telefone':'Tipo de Telefone',
        }

        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'phone_ddd'}),

        }

class EnderecoForm(forms.ModelForm):

    class Meta:
        model = Endereco
        fields = (
            'cep',
            'logradouro',
            'bairro',
            'municipio',
            'uf',


        )

        widgets = {
            'logradouro': forms.TextInput(attrs={'readonly': 'readonly', }),
            'bairro': forms.TextInput(attrs={'readonly': 'readonly'}),
            'municipio': forms.TextInput(attrs={'readonly': 'readonly'}),
            'uf': forms.TextInput(attrs={'readonly': 'readonly'}),
            'cep': forms.TextInput(attrs={'class': 'cep'}),

        }

        labels = {
            'cep':'CEP',
            'uf':'UF'

        }



EnderecoFormSet = inlineformset_factory(Usuario, Endereco, form=EnderecoForm, extra=1, can_delete=False)
TelefoneFormSet = inlineformset_factory(Usuario, Telefone, form=TelefoneForm, extra=1, can_delete=False)
