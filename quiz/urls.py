from django.urls import path
from . import views
from django.views.generic.base import TemplateView

from .views import (
    QuizHomeView,
    QuizSettingView,
    QuizView,
    QuizResultView,
)

app_name = 'quiz'

urlpatterns = [
    path('', QuizHomeView.as_view(), name='quiz_home'),
    path('setting', QuizSettingView.as_view(), name='quiz_setting'),
    path('question/<int:user_vocab_id>', QuizView.as_view(), name='quiz_question'),
    path('result/<int:user_vocab_id>', QuizResultView.as_view(), name='quiz_result'),
]
