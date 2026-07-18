from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import UserEventIsReadedUpdateForm

from .models import Event, UserEvent

from .service.event import EventService

class UserEventListView(LoginRequiredMixin, ListView):
    model = UserEvent
    template_name = 'core/event/user_event_list.html'
    context_object_name = 'user_events'
    ordering = ['pk']
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