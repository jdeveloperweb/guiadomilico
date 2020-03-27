from django.contrib.auth import login, logout
from django.core.validators import validate_email

from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from django.shortcuts import render

from guiadomilico.apps.accounts.models.base import Usuario
from guiadomilico.apps.accounts.forms.login import LoginForm

# Create your views here.

class LoginView(FormView):
	success_url = reverse_lazy('core:index')
	form_class = LoginForm
	template_name = 'accounts/login.html'

	@method_decorator(sensitive_post_parameters('password'))
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		request.session.set_test_cookie()
		logout(request)

		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		login(self.request, form.get_user())

		if self.request.session.test_cookie_worked():
			self.request.session.delete_test_cookie()

		return super(LoginView, self).form_valid(form)

