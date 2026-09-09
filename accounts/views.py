import logging

from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.cache import cache

from .tokens import account_activation_token

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
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

from django.contrib import messages

from django.utils import timezone
from django.utils.decorators import method_decorator

from .forms import (
    RegistForm,
    UserLoginForm,
    ResendActivationEmailForm,
)


from dictionary.service.user_vocab_action import UserVocabService
from core.service.event import EventService

logger = logging.getLogger(__name__)

User = get_user_model()

def send_activation_email(*, request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    token = account_activation_token.make_token(user)

    activation_path = reverse(
        "accounts:user_activate",
        kwargs={
            "uidb64": uidb64,
            "token": token,
        },
    )

    activation_url = request.build_absolute_uri(activation_path)

    email_context = {
        "user": user,
        "activation_url": activation_url,
    }

    subject = render_to_string(
        "accounts/email/user_activation_subject.txt",
        email_context,
    ).strip()

    message = render_to_string(
        "accounts/email/user_activation_body.txt",
        email_context,
    )
    try:
        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Activation email sending failed: "
            "operation=%s user_id=%s",
            "activation_email_send",
            user.pk,
        )
        return False

    if sent_count != 1:
        logger.error(
            "Activation email was not sent: "
            "operation=%s user_id=%s sent_count=%s",
            "activation_email_send",
            user.pk,
            sent_count,
        )
        return False

    if settings.DEBUG:
        print(f"Development activation URL: {activation_url}")

    return True


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_home.html'

class RegistUserView(CreateView):
    template_name = 'accounts/user_regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:activation_email_sent')

    def form_valid(self, form):
        result = super().form_valid(form)

        email_sent = send_activation_email(request=self.request, user=self.object)

        if not email_sent:
            messages.error(
                self.request,
                "認証メールを送信できませんでした。しばらくしてから再送してください。",
            )
            return redirect("accounts:resend_activation_email")

        cache.set(
            f"activation-email-resend:{self.object.pk}",
            True,
            timeout=settings.ACTIVATION_EMAIL_RESEND_COOLDOWN_SECONDS,
        )
        logger.info(
            "User registration completed: "
            "operation=%s user_id=%s activation_email_sent=%s",
            "user_registration",
            self.object.pk,
            True
        )
        return result

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('accounts:user_home')

    def form_valid(self, form):
        result = super().form_valid(form)
        remember = form.cleaned_data['remember_me']

        UserVocabService.sync_vocab_safely(user=self.request.user)
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(60 * 60)

        logger.info(
            "User login completed: "
            "operation=%s user_id=%s remember_me=%s",
            "user_login",
            self.request.user.pk,
            remember,
        )
        return result

class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/user_logout.html'
    next_page = reverse_lazy('accounts:user_home')

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        UserVocabService.sync_vocab_safely(user=self.request.user)
        return super().get_context_data(**kwargs)

class ActivationEmailSentView(TemplateView):
    template_name = "accounts/activation_email_sent.html"

class ActivateUserView(View):
    template_name = "accounts/user_activate.html"

    def get_user(self, uidb64):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is None:
            raise Http404

        if user.is_active:
            return render(
                request,
                self.template_name,
                context={
                    "activation_status": "already_active"
                },
            )

        if not account_activation_token.check_token(user, token):
            return render(
                request,
                self.template_name,
                context={
                    "activation_status": "invalid"
                },
                status=400,
            )

        return render(
            request,
            self.template_name,
            context={
                "activation_status":"confirm"
            },
        )

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is None:
            raise Http404

        if user.is_active:
            return render(
                request,
                self.template_name,
                context={
                    "activation_status": "already_active"
                },
            )

        if not account_activation_token.check_token(user, token):
            return render(
                request,
                self.template_name,
                context={
                    "activation_status": "invalid"
                },
                status=400,
            )

        user.is_active = True
        user.save(update_fields=["is_active"])

        UserVocabService.sync_vocab_safely(user=user)

        logger.info(
            "User account activated: operation=%s user_id=%s",
            "user_account_activation",
            user.pk,
        )

        return render(
            request,
            self.template_name,
            context={
                "activation_status": "success"
            },
        )

class ResendActivationEmailView(FormView):
    template_name = "accounts/resend_activation_email.html"
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy("accounts:activation_email_sent")

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        user = User.objects.filter(
            email__iexact=email,
            is_active=False,
        ).first()

        if user is not None:
            cache_key = f"activation-email-resend:{user.pk}"

            can_send = cache.add(
                cache_key,
                True,
                timeout=settings.ACTIVATION_EMAIL_RESEND_COOLDOWN_SECONDS,
            )

            if can_send:
                email_sent = send_activation_email(
                    request=self.request,
                    user=user,
                )
                if not email_sent:
                    cache.delete(cache_key)
                else:
                    logger.info(
                        "Activation email resent: "
                        "operation=%s user_id=%s",
                        "activation_email_resend",
                        user.pk,
                    )
        return super().form_valid(form)
