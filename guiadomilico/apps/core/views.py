from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class ShopView(TemplateView):
    template_name = "core/shop.html"

    ## FALTA IMPLEMENTAR ##

class IndexView(TemplateView):
    template_name = "core/index.html"

    ## FALTA IMPLEMENTAR ##

class SucessView(TemplateView):
    template_name = "accounts/active_sucess.html"

    ## FALTA IMPLEMENTAR ##




