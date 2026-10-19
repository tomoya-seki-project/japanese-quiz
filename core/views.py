import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from django.core.exceptions import ValidationError

from django.db import transaction, DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views.generic import ListView, FormView, View
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from .forms import (
    UserEventIsReadedUpdateForm,
    UserEventReadStatusUpdateForm,
    FeedbackCreateForm,
    FeedbackReplyForm,
    FeedbackListFilterForm,
)

from .models import Event, EventType, UserEvent, Feedback, FeedbackType, FeedbackStatus

from .service.event import EventService
from .service.feedback import FeedbackService

logger = logging.getLogger(__name__)

@never_cache
@require_safe
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        logger.exception(
            "Health check database failure: operation=%s",
            "health_check_database",
        )
        return JsonResponse(
            {"status": "unhealthy"},
            status=503,
        )
    return JsonResponse({"status":"ok"})


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
        if not form.is_valid():
            logger.warning(
                "User event selection rejected: "
                "operation=%s user_id=%s errors=%s",
                "user_event_mark_read",
                request.user.pk,
                form.errors.as_json(),
            )
            messages.error(
                request,
                "お知らせの選択内容を確認できませんでした。ページを再読み込みして、もう一度お試しください。",
            )
            return redirect(request.get_full_path())

        selectable_ids = form.cleaned_data["selectable_ids"]
        selected_ids = form.cleaned_data["selected_ids"]
        updated_count = EventService.set_user_event_status(
            user=request.user,
            selected_ids=selected_ids,
            selectable_ids=selectable_ids,
        )
        if updated_count > 0:
            logger.info(
                "User events marked as read: "
                "operation=%s user_id=%s updated_count=%s",
                "user_event_mark_read",
                request.user.pk,
                updated_count,
            )
            messages.success(
                request,
                "選択したお知らせを既読にしました。",
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

        return qs.select_related("event")

class UserEventDetailView(LoginRequiredMixin, DetailView):
    model = UserEvent
    template_name = 'core/event/user_event_detail.html'
    context_object_name = 'user_event'
    pk_url_kwarg = "user_event_pk"

    def get_return_url(self):
        next_url = self.request.GET.get("next")

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url

        return reverse("core:user_event_list")

    def post(self, request, *args, **kwargs):

        form = UserEventReadStatusUpdateForm(
            request.POST
        )
        if not form.is_valid():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            context["read_status_form"] = form

            return self.render_to_response(
                context,
                status=400
            )

        action = form.cleaned_data["action"]
        user_event = self.get_queryset().filter(
            pk=self.kwargs["user_event_pk"],
        )
        if action == "mark_read":
            updated_count = user_event.filter(is_read=False).update(
                                is_read=True,
                                read_at=timezone.now(),
                            )
            success_message = "既読にしました"
        else:
            updated_count = user_event.filter(is_read=True).update(
                                is_read=False,
                                read_at=None,
                            )
            success_message = "未読に戻しました"

        if updated_count == 0:
            self.get_object()

        messages.success(request, success_message)
        return redirect(request.get_full_path())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.get_return_url()
        return context

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
        messages.success(
            self.request,
            "フィードバックを送信しました。",
        )
        return super().form_valid(form)

class FeedbackListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "core/feedback/feedback_list.html"
    model = Feedback
    context_object_name = "feedbacks"
    ordering = ["-create_at"]
    paginate_by = 5

    def get_filter_form(self):
        if hasattr(self, "_feedback_filter_form"):
            return self._feedback_filter_form

        raw_status = self.request.GET.get("status", FeedbackStatus.PENDING)

        form = FeedbackListFilterForm({
            "status": raw_status,
        })

        if form.is_valid() and form.cleaned_data["status"]:
            selected_status = form.cleaned_data["status"]
        else:
            selected_status = FeedbackStatus.PENDING
            form = FeedbackListFilterForm({
                "status": selected_status,
            })

        self._selected_status = selected_status
        self._feedback_filter_form = form
        return form

    def get_selected_status(self):
        self.get_filter_form()
        return self._selected_status

    def get_queryset(self):
        queryset = super().get_queryset().select_related("user", "reply_by")

        selected_status = self.get_selected_status()

        if selected_status != "all":
            queryset = queryset.filter(status=selected_status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.get_filter_form()
        context["selected_status"] = self.get_selected_status()
        return context

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

    def get_return_url(self):
        next_url = self.request.GET.get("next")

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url

        return reverse("core:feedback_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["return_url"] = self.get_return_url()
        return context

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

    def get_queryset(self):
        return super().get_queryset().select_related("user","reply_by")

class FeedbackReplyView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "core/feedback/feedback_reply.html"
    form_class = FeedbackReplyForm

    def get_feedback(self):
        if not hasattr(self, "_feedback"):
            self._feedback = get_object_or_404(
                Feedback.objects.select_related("user"),
                pk=self.kwargs["feedback_pk"],
            )
        return self._feedback

    def get(self, request, *args, **kwargs):
        if self.get_feedback().status == FeedbackStatus.CLOSED:
            messages.info(request, "このフィードバックはすでに終了しています。")
            return redirect(self.get_return_url())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.get_feedback().status == FeedbackStatus.CLOSED:
            messages.info(request, "このフィードバックはすでに終了しています。")
            return redirect(self.get_return_url())
        return super().post(request, *args, **kwargs)

    def get_return_url(self):
        next_url = self.request.GET.get("next")

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url

        return reverse(
            "core:feedback_detail",
            kwargs={"pk": self.kwargs["feedback_pk"]},
        )

    def get_success_url(self):
        return self.get_return_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback"] = self.get_feedback()
        context["return_url"] = self.get_return_url()
        return context

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
                target_feedback=self.get_feedback(),
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
                f"フィードバック #{self.kwargs['feedback_pk']} への返信を送信しました。"
            )
        return super().form_valid(form)
