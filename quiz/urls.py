from django.urls import path
from . import views
from django.views.generic.base import TemplateView

from .views import (
    QuizHomeView,
    QuizSettingView,
    QuizPlayView,
    QuizSubmitAnswerView,
    QuizNextView,
    QuizSkipView,
    QuizUnfinishedView,
    QuizSummaryView,
    QuizNoPoolConfirmView
)

app_name = 'quiz'

urlpatterns = [
    path('', QuizHomeView.as_view(), name='quiz_home'),
    path('setting', QuizSettingView.as_view(), name='quiz_setting'),
    path('play', QuizPlayView.as_view(), name='quiz_play'),
    path('submit_answer', QuizSubmitAnswerView.as_view(), name='quiz_submit_answer'),
    path('next/', QuizNextView.as_view(), name='quiz_next'),
    path('skip/', QuizSkipView.as_view(), name='quiz_skip'),
    path('unfinished/', QuizUnfinishedView.as_view(), name='quiz_unfinished'),
    path('summary/', QuizSummaryView.as_view(), name='quiz_summary'),
    path('no_pool_confirm/', QuizNoPoolConfirmView.as_view(), name='quiz_no_pool_confirm'),
]
