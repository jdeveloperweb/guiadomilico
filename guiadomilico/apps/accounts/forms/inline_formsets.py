# -*- coding: utf-8 -*-

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from guiadomilico.apps.accounts.models import Telefone


class TelefoneForm(forms.ModelForm):

    class Meta:
        model = Telefone
        fields = ('tipo_telefone', 'telefone',)