from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from guiadomilico.apps.blog.models import Post


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'dashboard/post_list.html', {'posts': posts})
