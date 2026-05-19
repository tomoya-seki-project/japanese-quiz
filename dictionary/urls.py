from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'dictionary'

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/temp.html'), name='temp'),
]
