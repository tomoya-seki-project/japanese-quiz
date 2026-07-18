from django.urls import path
from . import views
from django.views.generic.base import TemplateView

from .views import (
    UserEventDetailView,
    UserEventListView,
)

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/temp.html'), name='temp'),
    path('user_event_list', UserEventListView.as_view(), name='user_event_list'),
    path('user_event_detail/<int:pk>', UserEventDetailView.as_view(), name='user_event_detail'),
]
