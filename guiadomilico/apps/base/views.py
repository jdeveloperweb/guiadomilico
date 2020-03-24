from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class ShopView(TemplateView):
    template_name = "base/shop.html"

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        return context

class IndexView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


