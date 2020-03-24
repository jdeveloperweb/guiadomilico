from __future__ import unicode_literals
import re

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .constants import *


class Pessoa(models.Model):

    # Dados
    nome = models.CharField(max_length=255, null=True, blank=True)
    nome_razao_social = models.CharField(max_length=255, null=True, blank=True)
    tipo_pessoa = models.CharField(max_length=2, choices=TIPO_PESSOA)
    inscricao_municipal = models.CharField(
        max_length=32, null=True, blank=True)
    informacoes_adicionais = models.CharField(
        max_length=1055, null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO, null=True, blank=True)

    # Regras de acesso
    role = models.PositiveSmallIntegerField(default=9, choices=PAPEIS)


    # Dados padrao
    endereco_padrao = models.ForeignKey(
        'accounts.Endereco', related_name="end_padrao", on_delete=models.CASCADE, null=True, blank=True)
    telefone_padrao = models.ForeignKey(
        'accounts.Telefone', related_name="tel_padrao", on_delete=models.CASCADE, null=True, blank=True)
    site_padrao = models.ForeignKey(
        'accounts.Site', related_name="sit_padrao", on_delete=models.CASCADE, null=True, blank=True)
    email_padrao = models.ForeignKey(
        'accounts.Email', related_name="ema_padrao", on_delete=models.CASCADE, null=True, blank=True)


    # Sobre o objeto
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(editable=False)
    data_edicao = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Atualizar datas criacao edicao
        if not self.data_criacao:
            self.data_criacao = timezone.now()
        self.data_edicao = timezone.now()
        return super(Pessoa, self).save(*args, **kwargs)

    @property
    def cpf_cnpj_apenas_digitos(self):
        if self.tipo_pessoa == 'PF':
            if self.pessoa_fis_info.cpf:
                return re.sub('[./-]', '', self.pessoa_fis_info.cpf)

        elif self.tipo_pessoa == 'PJ':
            if self.pessoa_jur_info.cnpj:
                return re.sub('[./-]', '', self.pessoa_jur_info.cnpj)

        else:
            return ''

    @property
    def inscricao_estadual(self):
        if self.tipo_pessoa == 'PF':
            return 'ISENTO'
        elif self.tipo_pessoa == 'PJ':
            if self.pessoa_jur_info.inscricao_estadual:
                return re.sub('[./-]', '', self.pessoa_jur_info.inscricao_estadual)
        else:
            return ''

    @property
    def uf_padrao(self):
        if self.endereco_padrao:
            return self.endereco_padrao.uf
        else:
            return ''

    def __unicode__(self):
        s = u'%s' % (self.nome_razao_social)
        return s

    def __str__(self):
        s = u'%s' % (self.nome_razao_social)
        return s


class PessoaFisica(models.Model):
    pessoa_id = models.OneToOneField(
        Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='pessoa_fis_info')
    cpf = models.CharField(name='CPF', max_length=32, null=True, blank=True)
    rg = models.CharField(max_length=32, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)

    @property
    def format_cpf(self):
        if self.cpf:
            return 'CPF: {}'.format(self.cpf)
        else:
            return ''

    @property
    def format_rg(self):
        if self.rg:
            return 'RG: {}'.format(self.rg)
        else:
            return ''


class PessoaJuridica(models.Model):
    pessoa_id = models.OneToOneField(
        Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='pessoa_jur_info')
    cnpj = models.CharField(max_length=32, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True)
    inscricao_estadual = models.CharField(max_length=32, null=True, blank=True)
    responsavel = models.CharField(max_length=32, null=True, blank=True)
    sit_fiscal = models.CharField(
        max_length=2, null=True, blank=True, choices=ENQUADRAMENTO_FISCAL)
    suframa = models.CharField(max_length=16, null=True, blank=True)

    @property
    def format_cnpj(self):
        if self.cnpj:
            return 'CNPJ: {}'.format(self.cnpj)
        else:
            return ''

    @property
    def format_ie(self):
        if self.inscricao_estadual:
            return 'IE: {}'.format(self.inscricao_estadual)
        else:
            return ''

    @property
    def format_responsavel(self):
        if self.responsavel:
            return 'Representante: {}'.format(self.responsavel)
        else:
            return ''


class Endereco(models.Model):
    pessoa_end = models.ForeignKey(
        Pessoa, related_name="endereco", on_delete=models.CASCADE)
    tipo_endereco = models.CharField(
        max_length=3, null=True, blank=True, choices=TIPO_ENDERECO)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=16, null=True, blank=True)
    bairro = models.CharField(max_length=64, null=True, blank=True)
    complemento = models.CharField(max_length=64, null=True, blank=True)
    pais = models.CharField(max_length=32, null=True,
                            blank=True, default='Brasil')
    codigo_pais = models.CharField(max_length=5, null=True,
                             blank=True, default='1058')
    municipio = models.CharField(max_length=64, null=True, blank=True)
    codigo_mun = models.CharField(max_length=9, null=True, blank=True)
    cep = models.CharField(max_length=16, null=True, blank=True)
    uf = models.CharField(max_length=3, null=True,
                          blank=True, choices=UF_SIGLA)

    @property
    def format_endereco(self):
        return '{0}, {1} - {2}'.format(self.logradouro, self.numero, self.bairro)

    @property
    def format_endereco_completo(self):
        return '{0} - {1} - {2} - {3} - {4} - {5} - {6}'.format(self.logradouro, self.numero, self.bairro, self.municipio, self.cep, self.uf, self.pais)

    def __unicode__(self):
        s = u'%s, %s, %s (%s)' % (
            self.logradouro, self.numero, self.municipio, self.uf)
        return s

    def __str__(self):
        s = u'%s, %s, %s (%s)' % (
            self.logradouro, self.numero, self.municipio, self.uf)
        return s


class Telefone(models.Model):
    pessoa_tel = models.ForeignKey(
        Pessoa, related_name="telefone", on_delete=models.CASCADE)
    tipo_telefone = models.CharField(
        max_length=8, choices=TIPO_TELEFONE, null=True, blank=True)
    telefone = models.CharField(max_length=32)

    def get_telefone_apenas_digitos(self):
        return self.telefone.replace('(', '').replace(' ', '').replace(')', '').replace('-', '')

    def __str__(self):
        s = u'%s / %s' % (
            self.telefone.replace('(', '').replace(' ', '').replace(')', '').replace('-', ''),
            self.tipo_telefone
            )
        return s

class Email(models.Model):
    pessoa_email = models.ForeignKey(
        Pessoa, related_name="email", on_delete=models.CASCADE)
    email = models.CharField(max_length=255)

    def __str__(self):
        s = u'%s' % (self.email )
        return s

class Site(models.Model):
    pessoa_site = models.ForeignKey(
        Pessoa, related_name="site", on_delete=models.CASCADE)
    site = models.CharField(max_length=255)

    def __str__(self):
        s = u'%s' % (self.site )
        return s

class Banco(models.Model):
    pessoa_banco = models.ForeignKey(
        Pessoa, related_name="banco", on_delete=models.CASCADE)
    banco = models.CharField(
        max_length=3, choices=BANCOS, null=True, blank=True)
    agencia = models.CharField(max_length=8, null=True, blank=True)
    conta = models.CharField(max_length=32, null=True, blank=True)
    digito = models.CharField(max_length=8, null=True, blank=True)

    def __unicode__(self):
        s = u'%s / %s / %s' % (self.get_banco_display(),
                               self.agencia, self.conta)
        return s

    def __str__(self):
        s = u'%s / %s / %s' % (self.get_banco_display(),
                               self.agencia, self.conta)
        return s


class Documento(models.Model):
    pessoa_documento = models.ForeignKey(
        Pessoa, related_name="documento", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=32)
    documento = models.CharField(max_length=255)

    def __str__(self):
        s = u'%s' % (self.documento )
        return s