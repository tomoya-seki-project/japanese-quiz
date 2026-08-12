from django.urls import path
from . import views
from django.views.generic.base import TemplateView

from .views import (
    UserEventDetailView,
    UserEventListView,
    FAQCreateView,
    FAQDetailView,
    FAQListView,
)

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/temp.html'), name='temp'),
    path('user_event_list', UserEventListView.as_view(), name='user_event_list'),
    path('user_event_detail/<int:pk>', UserEventDetailView.as_view(), name='user_event_detail'),
    path('FAQ_create/', FAQCreateView.as_view(), name='FAQ_create'),
    path('FAQ_list/', FAQListView.as_view(), name='FAQ_list'),
    path('FAQ_detail/<int:pk>', FAQDetailView.as_view(), name='FAQ_detail'),

]
