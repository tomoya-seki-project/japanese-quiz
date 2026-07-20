from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import (
    TemplateView,
    FormView,
)

from .forms import (
    QuizSettingForm,
    QuizForm,
)

from dictionary.models import (
    UserVocab,
    VocabType,
)

from .service.quiz import QuizService

class QuizHomeView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/quiz_home.html"

class QuizSettingView(LoginRequiredMixin, FormView):
    template_name = "quiz/quiz_setting.html"
    form_class = QuizSettingForm
    user_vocab_id = 0

    def form_valid(self, form):
        question_pool_qs = QuizService.create_question_pool(
            user=self.request.user,
            vocab_type=form.cleaned_data.get("vocab_type"),
            level=form.cleaned_data.get("level"),
            categories=form.cleaned_data.get("categories"),
        )
        user_vocab_id = QuizService.pick_random_vocab(
            user=self.request.user,
            queryset=question_pool_qs,
        )
        return redirect("quiz:quiz_question", user_vocab_id=user_vocab_id)
    
class QuizView(LoginRequiredMixin, FormView):
    template_name = "quiz/quiz_question.html"
    form_class = QuizForm
    
    def form_valid(self, form):
        target_vocab = get_object_or_404(UserVocab, pk=self.kwargs["user_vocab_id"], user=self.request.user)
        if target_vocab.vocab.type == VocabType.VOCAB:
            result = QuizService.check_kana_answer(
                question_vocab=target_vocab,
                answer=form.cleaned_data.get("answer"),
                tips_count=form.cleaned_data.get("tips_count"),
            )
        return redirect("quiz:quiz_result", user_vocab_id=target_vocab.pk)
    

class QuizResultView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/quiz_result.html"
    
