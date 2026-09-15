import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from django.core.exceptions import ValidationError

from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views.generic import ListView, FormView, View
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from .forms import UserEventIsReadedUpdateForm, FeedbackCreateForm, FeedbackReplyForm

from .models import Event, EventType, UserEvent, Feedback, FeedbackType, FeedbackStatus

from .service.event import EventService
from .service.feedback import FeedbackService

logger = logging.getLogger(__name__)


class UserEventListView(LoginRequiredMixin, ListView):
    model = UserEvent
    template_name = 'core/event/user_event_list.html'
    context_object_name = 'user_events'
    ordering = ['-event__create_at']
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        user_event_queryset = self.get_queryset()

        form = UserEventIsReadedUpdateForm(
            request.POST,
            user_event_queryset=user_event_queryset,
        )
        if form.is_valid():
            selectable_ids = form.cleaned_data["selectable_ids"]
            selected_ids = form.cleaned_data["selected_ids"]

            selectable_qs = UserEvent.objects.filter(
                user=request.user,
                is_read=False,
                id__in=selectable_ids,
            )
            get_select_qs = selectable_qs.filter(
                id__in=selected_ids,
            )
            now = timezone.now()
            updated_count = get_select_qs.update(is_read=True, read_at=now)
            if updated_count > 0:
                logger.info(
                    "User events marked as read: "
                    "operation=%s user_id=%s updated_count=%s",
                    "user_event_mark_read",
                    request.user.pk,
                    updated_count,
                )
        return redirect(request.get_full_path())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["query_string"] = query_params.urlencode()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'core/event/partials/user_event_list_partial.html', context)
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)

        status = self.request.GET.get("status")

        if status == "read":
            qs = qs.filter(is_read=True)
        elif status == "unread":
            qs = qs.filter(is_read=False)

        return qs

class UserEventDetailView(LoginRequiredMixin, DetailView):
    model = UserEvent
    template_name = 'core/event/user_event_detail.html'
    context_object_name = 'user_event'

    def get_queryset(self):
        return UserEvent.objects.filter(user=self.request.user).select_related('event')

class FeedbackView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("core:feedback_create")

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return reverse("core:feedback_list")
        return super().get_redirect_url(*args, **kwargs)

class FeedbackCreateView(LoginRequiredMixin, FormView):
    template_name = "core/feedback/feedback_create.html"
    form_class = FeedbackCreateForm
    success_url = reverse_lazy("HomePage")

    def form_valid(self, form):
        feedback_type = form.cleaned_data["feedback_type"]
        context = form.cleaned_data["context"]
        user_feedback, is_doubled = FeedbackService.create_feedback(
            user=self.request.user,
            feedback_type=feedback_type,
            context=context
        )
        if is_doubled:
            logger.info(
                "Feedback submission skipped: "
                "operation=%s user_id=%s feedback_type=%s reason=%s",
                "feedback_create",
                self.request.user.pk,
                feedback_type,
                "duplicate_pending_feedback",
            )
            messages.warning(
                self.request,
                "同じ内容のフィードバックはすでに送信されています。管理者の確認をお待ちください。"
            )
            form.add_error(None, "このフィードバックは送信済みです。管理者の確認をお待ちください。")
            return self.form_invalid(form)
        logger.info(
            "Feedback created: "
            "operation=%s user_id=%s feedback_id=%s feedback_type=%s",
            "feedback_create",
            self.request.user.pk,
            user_feedback.pk,
            feedback_type,
        )
        return super().form_valid(form)

class FeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "core/feedback/feedback_list.html"
    model = Feedback
    context_object_name = "feedbacks"
    ordering = ["-create_at"]
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        logger.warning(
            "Feedback admin access denied: "
            "operation=%s user_id=%s view=%s",
            "feedback_admin_access",
            self.request.user.pk,
            self.__class__.__name__,
        )
        return redirect("HomePage")

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'core/feedback/partials/feedback_list_partial.html', context)
        return super().render_to_response(context, **response_kwargs)


class FeedbackDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "core/feedback/feedback_detail.html"
    model = Feedback
    context_object_name = "feedback"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        logger.warning(
            "Feedback admin access denied: "
            "operation=%s user_id=%s view=%s",
            "feedback_admin_access",
            self.request.user.pk,
            self.__class__.__name__,
        )
        return redirect("HomePage")

class FeedbackReplyView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "core/feedback/feedback_reply.html"
    form_class = FeedbackReplyForm
    success_url = reverse_lazy("HomePage")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        logger.warning(
            "Feedback admin access denied: "
            "operation=%s user_id=%s view=%s",
            "feedback_admin_access",
            self.request.user.pk,
            self.__class__.__name__,
        )
        return redirect("HomePage")

    def form_valid(self, form):
        is_close = form.cleaned_data["is_close"]
        context = form.cleaned_data["context"]
        try:
            reply_event = FeedbackService.reply_feedback(
                admin_user=self.request.user,
                target_feedback=get_object_or_404(Feedback, pk=self.kwargs["feedback_pk"]),
                reply_context=context,
                is_close=is_close
            )
        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)
        if reply_event is not None:
            logger.info(
                "Feedback reply completed: "
                "operation=%s admin_user_id=%s feedback_id=%s event_id=%s",
                "feedback_reply",
                self.request.user.pk,
                self.kwargs["feedback_pk"],
                reply_event.pk,
            )
            messages.success(
                self.request,
                f"Your reply to feedback #{self.kwargs['feedback_pk']} has been sent."
            )
        return super().form_valid(form)

