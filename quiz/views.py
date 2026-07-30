from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.conf import settings

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
    QuizSkipForm,
)

from dictionary.models import (
    UserVocab,
    VocabType,
)

from .service.quiz import QuizService
from .constants import HIRAGANA_ROWS, KATAKANA_ROWS

def get_input_panel_rows(*, question_vocab):
    if question_vocab.vocab.type == VocabType.VOCAB:
        keyboard_rows = HIRAGANA_ROWS
        mc_rows = None
    elif question_vocab.vocab.type == VocabType.KATAKANA:
        keyboard_rows = KATAKANA_ROWS
        mc_rows = None
    else:
        keyboard_rows = None
        mc_rows = ["A", "B", "C", "D", "E"]
    return keyboard_rows, mc_rows

def render_quiz_question_payload_html(*, request, target_vocab, fallback_used):
    keyboard_rows, mc_rows = get_input_panel_rows(question_vocab = target_vocab)
    main_html = render_to_string(
        "quiz/partials/quiz_question_partial.html",
        context={
            "question_vocab": target_vocab,
            "fallback_used": fallback_used,
        },
        request=request,
    )
    input_panel_html = render_to_string(
        "quiz/partials/quiz_input_panel_partial.html",
        context={
            "keyboard_rows": keyboard_rows,
            "mc_rows":mc_rows,
        },
        request=request
    )
    return main_html, input_panel_html

def build_next_question_payload(*, request):
    settings = request.session.get("quiz_settings")

    question_pool_qs, fallback_used = QuizService.create_question_pool(
        user=request.user,
        vocab_type=settings["vocab_type"],
        level=settings["level"],
        categories=settings["categories"],
    )

    if fallback_used:
        messages.warning(
            request,
            "No vocab matched your selected filters, so the quiz is using your full active vocab pool."
        )
        return {
            "main_html": render_to_string(
                "quiz/partials/quiz_no_question_partial.html",
                request=request,
            ),
            "input_panel_html": "",
        }

    user_vocab_id = QuizService.pick_random_vocab(
        user=request.user,
        queryset=question_pool_qs,
    )

    if user_vocab_id is None:
        return {
            "main_html": render_to_string(
                "quiz/partials/quiz_no_question_partial.html",
                request=request,
            ),
            "input_panel_html": "",
        }

    request.session["question_vocab"] = {
        "user_vocab_id": user_vocab_id,
        "fallback_used": fallback_used,
    }

    target_vocab = get_object_or_404(
        UserVocab,
        pk=user_vocab_id,
        user=request.user,
    )

    main_html, input_panel_html = render_quiz_question_payload_html(
        request=request,
        target_vocab=target_vocab,
        fallback_used=fallback_used,
    )

    return {
        "main_html": main_html,
        "input_panel_html": input_panel_html,
    }

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

    def get(self, request, *args, **kwargs):
        in_use_count = UserVocab.objects.filter(user=request.user, in_use=True).count()

        min_count = getattr(settings, "QUIZ_MIN_IN_USE_VOCAB_COUNT", 10)
        if in_use_count < min_count:
            messages.warning(
                request,
                f"You need at least {min_count} active vocab items before starting a quiz. Please enable more vocab items first."
            )
            return redirect("dictionary:user_vocab_list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        level = form.cleaned_data["level"]
        vocab_type = form.cleaned_data["vocab_type"]
        categories = list(form.cleaned_data["categories"].values_list("id", flat=True))
        if form.cleaned_data["use_last_setting"] == True:
            settings = self.request.session.get("quiz_settings")
            level=settings["level"]
            vocab_type=settings["vocab_type"]
            categories=settings["categories"]
            
        self.request.session["quiz_settings"] = {
            "level": level,
            "vocab_type": vocab_type,
            "categories": categories,
        }
        return redirect("quiz:quiz_play")
    
class QuizPlayView(LoginRequiredMixin, QuizSettingRequiredMixin, TemplateView):
    template_name = "quiz/quiz_play.html"

    def get(self, request, *args, **kwargs):
        settings = self.request.session.get("quiz_settings")
        question_pool_qs, fallback_used = QuizService.create_question_pool(
            user=self.request.user,
            vocab_type=settings["vocab_type"],
            level=settings["level"],
            categories=settings["categories"],
        )
        user_vocab_id = QuizService.pick_random_vocab(
            user=self.request.user,
            queryset=question_pool_qs,
        )
        if user_vocab_id is None:
            messages.warning(
                request,
                "No active vocab is available for this quiz. Please enable vocab items first."
            )
            return redirect("dictionary:user_vocab_list")
        
        self.request.session["question_vocab"] = {
            "user_vocab_id": user_vocab_id,
            "fallback_used": fallback_used,
        }
        self.question_vocab = get_object_or_404(UserVocab, pk=user_vocab_id, user=self.request.user)
        self.fallback_used = fallback_used
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyboard_rows, mc_rows = get_input_panel_rows(question_vocab = self.question_vocab)
            
        context["question_vocab"] = self.question_vocab
        context["fallback_used"] = self.fallback_used
        context["keyboard_rows"] = keyboard_rows
        context["mc_rows"] = mc_rows
        return context

class QuizSubmitAnswerView(LoginRequiredMixin, QuizSettingRequiredMixin, FormView):
    form_class = QuizForm

    def form_valid(self, form):
        question_vocab = get_object_or_404(
            UserVocab, 
            pk=form.cleaned_data.get("user_vocab_id"), 
            user=self.request.user
        )        
        question_data = self.request.session.get("question_vocab",{})
        fallback_used = question_data.get("fallback_used",False)
        is_correct = False
        if question_vocab.vocab.type == VocabType.VOCAB:
            is_correct = QuizService.check_kana_answer(
                question_vocab=question_vocab,
                answer=form.cleaned_data.get("answer"),
                tips_count=form.cleaned_data.get("tips_count"),
            )
        main_html = render_to_string(
            "quiz/partials/quiz_result_partial.html",
            context={
                "question_vocab":question_vocab,
                "fallback_used":fallback_used,
                "is_correct":is_correct,
            },
            request=self.request,
        )
        return JsonResponse({
                    "main_html": main_html,
                    "input_panel_html": "",
                })

class QuizNextView(LoginRequiredMixin, QuizSettingRequiredMixin, FormView):
    form_class = QuizNextForm

    def form_valid(self, form):
        payload = build_next_question_payload(request=self.request)
        return JsonResponse(payload)

class QuizSkipView(LoginRequiredMixin, QuizSettingRequiredMixin, FormView):
    form_class = QuizSkipForm

    def form_valid(self, form):
        skipped_question_vocab = self.request.session.get("question_vocab")
        if skipped_question_vocab is not None:
            QuizService.skip_question_punish(user=self.request.user, user_vocab_id=skipped_question_vocab["user_vocab_id"])

        payload = build_next_question_payload(request=self.request)
        return JsonResponse(payload)
    
