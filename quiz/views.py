from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import (
    TemplateView,
    FormView,
    View,
)

from .forms import (
    QuizSettingForm,
    QuizForm,
    QuizNextForm,
)

from dictionary.models import (
    UserVocab,
    VocabType,
)

from .service.quiz import QuizService

class QuizSettingRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("quiz_settings"):
            return redirect("quiz:quiz_setting")
        return super().dispatch(request, *args, **kwargs)

class QuizHomeView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/quiz_home.html"

class QuizSettingView(LoginRequiredMixin, FormView):
    template_name = "quiz/quiz_setting.html"
    form_class = QuizSettingForm

    def form_valid(self, form):
        self.request.session["quiz_settings"] = {
            "level": form.cleaned_data["level"],
            "vocab_type": form.cleaned_data["vocab_type"],
            "categories": list(
                form.cleaned_data["categories"].value_list("id", flat=True)
            )
        }
        return redirect("quiz:quiz_play")
    
class QuizPlayView(LoginRequiredMixin, QuizSettingRequiredMixin, TemplateView):
    template_name = "quiz/quiz_play.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = self.request.session.get("quiz_settings")
        question_pool_qs = QuizService.create_question_pool(
            user=self.request.user,
            vocab_type=settings["vocab_type"],
            level=settings["level"],
            categories=settings["categories"],
        )
        user_vocab_id = QuizService.pick_random_vocab(
            user=self.request.user,
            queryset=question_pool_qs,
        )
        self.request.session["question_vocab"] = {
            "user_vocab_id": user_vocab_id,
        }
        target_vocab = get_object_or_404(UserVocab, pk=user_vocab_id, user=self.request.user)
        context["question_vocab"] = target_vocab
        return context

class QuizSubmitAnswerView(LoginRequiredMixin, QuizSettingRequiredMixin, FormView):
    form_class = QuizForm

    def form_valid(self, form):
        question_vocab = get_object_or_404(
            UserVocab, 
            pk=form.cleaned_data.get("user_vocab_id"), 
            user=self.request.user
        )        
        if question_vocab.vocab.type == VocabType.VOCAB:
            QuizService.check_kana_answer(
                question_vocab=question_vocab,
                answer=form.cleaned_data.get("answer"),
                tips_count=form.cleaned_data.get("tips_count"),
            )
        return render(self.request, "quiz/partials/quiz_result_partial.html", 
                        context={"question_vocab":question_vocab})

class QuizNextView(LoginRequiredMixin, QuizSettingRequiredMixin, FormView):
    form_class = QuizNextForm

    def form_valid(self, form):
        #context = self.get_context_data()
        settings = self.request.session.get("quiz_settings")
        question_pool_qs = QuizService.create_question_pool(
            user=self.request.user,
            vocab_type=settings["vocab_type"],
            level=settings["level"],
            categories=settings["categories"],
        )
        user_vocab_id = QuizService.pick_random_vocab(
            user=self.request.user,
            queryset=question_pool_qs,
        )
        self.request.session["question_vocab"] = {
            "user_vocab_id": user_vocab_id,
        }
        target_vocab = get_object_or_404(UserVocab, pk=user_vocab_id, user=self.request.user)
        
        return render(self.request, "quiz/partials/quiz_question_partial.html", 
                      context = {
                            "question_vocab": target_vocab
                        })

    
