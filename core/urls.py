from django.urls import path
from . import views
from django.views.generic.base import TemplateView

from .views import (
    UserEventDetailView,
    UserEventListView,
    FeedbackView,
    FeedbackCreateView,
    FeedbackListView,
    FeedbackDetailView,
    FeedbackReplyView,
)

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/temp.html'), name='temp'),
    path('user_event_list', UserEventListView.as_view(), name='user_event_list'),
    path('user_event_detail/<int:pk>', UserEventDetailView.as_view(), name='user_event_detail'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('feedback/create/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback/list/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedback/detail/<int:pk>', FeedbackDetailView.as_view(), name='feedback_detail'),
    path('feedback/reply/<int:feedback_pk>', FeedbackReplyView.as_view(), name='feedback_reply'),

]
