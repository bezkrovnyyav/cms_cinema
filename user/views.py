from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, resolve
from django.views.generic import UpdateView, CreateView
from django.contrib.auth import logout
# import main.main_language
from .models import User
from cms.models import Client
from .forms import UserUpdateForm, UserLoginForm, CustomUserCreationForm
from django.utils.datetime_safe import datetime
from django.conf import settings
from cms.models import HomePage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect

# Create your views here.

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'user/pages/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        """Create an entry in the Client table for client device statistics"""
        date = datetime.now()
        Client.objects.get_or_create(
            date=date,
            user=self.request.user,
            is_mobile=self.request.user_agent.is_mobile,
            is_tablet=self.request.user_agent.is_tablet,
            is_pc=self.request.user_agent.is_pc
        )
        return HttpResponseRedirect('/' + self.request.user.language + '/')


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/pages/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, _('Вы успешно зарегистрированы можете авторизоваться!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _('Исправьте ошибки и попробуйте снова'))
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = UserUpdateForm
    model = User
    template_name = 'user/pages/client_page.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['home_page_data'] = HomePage.objects.all().first()
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _('Данные обновлены'))
        return HttpResponseRedirect('/' + form.cleaned_data['language'] + '/user')

    def form_invalid(self, form):
        messages.warning(self.request, _('Исправьте ошибки и попробуйте снова'))
        return super().form_invalid(form)


def user_logout(request):
    logout(request)
    return redirect('main')
