from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views.generic import ListView, FormView, View
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from .forms import UserEventIsReadedUpdateForm, FeedbackCreateForm, FeedbackReplyForm

from .models import Event, EventType, UserEvent, Feedback, FeedbackType, FeedbackStatus

from .service.event import EventService

class UserEventListView(LoginRequiredMixin, ListView):
    model = UserEvent
    template_name = 'core/event/user_event_list.html'
    context_object_name = 'user_events'
    ordering = ['pk']
    paginate_by = 5

    def get_template_names(self) -> list[str]:
        if self.get_queryset().count() == 0:
            return "core/event/no_unread_event.html"
        return super().get_template_names()
    

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
            get_select_qs.update(is_read=True, read_at=now)
        return redirect(request.get_full_path())
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'core/event/partials/user_event_list_partial.html', context)
        return super().render_to_response(context, **response_kwargs)
    
    def get_queryset(self):
        return EventService.get_unread_events(user=self.request.user)

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
        user_feedback, created = Feedback.objects.get_or_create(
            user=self.request.user,
            type=feedback_type,
            status=FeedbackStatus.PENDING,
            context=context,
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
        return redirect("HomePage")

class FeedbackReplyView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "core/feedback/feedback_reply.html"
    form_class = FeedbackReplyForm
    success_url = reverse_lazy("HomePage")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("HomePage")

    def form_valid(self, form):
        context = form.cleaned_data["context"]
        with transaction.atomic():
            reply_event = EventService.create_event(
                event_type=EventType.FEEDBACK_REPLY,
                event_title="Thank you for your feedback!",
                event_msg=context
            )
            target_feedback = get_object_or_404(Feedback, pk=self.kwargs['feedback_pk'])
            EventService.assign_event_to_user(
                user=target_feedback.user,
                event=reply_event,
            )    
            target_feedback.status = FeedbackStatus.REPLIED
            target_feedback.reply_by = self.request.user
            target_feedback.reply_at = timezone.now()
            target_feedback.update_at = timezone.now()
            target_feedback.save(update_fields=["status", "reply_by", "reply_at", "update_at"])
        return super().form_valid(form)
    

        

