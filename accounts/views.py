from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings

from django.views.generic import (
    CreateView,
    FormView,
    TemplateView,
)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.utils.decorators import method_decorator

from .forms import (
    RegistForm,
    UserLoginForm,
)

from dictionary.service.user_vocab_action import UserVocabService
from core.service.event import EventService

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_home.html'

class RegistUserView(CreateView):
    template_name = 'accounts/user_regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:user_home')
    
    def form_valid(self, form):
        result = super().form_valid(form)
        UserVocabService.sync_new_vocab(user=self.object)
        return result

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('accounts:user_home')

    def form_valid(self, form):
        result = super().form_valid(form)
        remember = form.cleaned_data['remember_me']

        UserVocabService.sync_new_vocab(user=self.request.user)
        EventService.gen_vocab_sync_event(user=self.request.user)
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(60 * 60)
        return result

class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/user_logout.html'
    next_page = reverse_lazy('accounts:user_home')

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        UserVocabService.sync_new_vocab(user=self.request.user)
        EventService.gen_vocab_sync_event(user=self.request.user)
        return super().get_context_data(**kwargs)
