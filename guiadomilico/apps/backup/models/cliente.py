# -*- coding: utf-8 -*-

from django.db import models

from .base import Pessoa



class Cliente(Pessoa):

    apelido = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome.__str__();