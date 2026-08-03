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

from .service.quiz import QuizService, load_quiz_config

from .constants import HIRAGANA_ROWS, KATAKANA_ROWS

QUIZ_CONFIG = load_quiz_config(path="config/quiz_config.json")


def get_question_pool(*, request):
    quiz_settings = request.session.get("quiz_settings")
    question_pool_qs, fallback_used = QuizService.create_question_pool(
        user=request.user,
        vocab_type=quiz_settings["vocab_type"],
        level=quiz_settings["level"],
        categories=quiz_settings["categories"],
    )
    return question_pool_qs, fallback_used

def get_target_user_vocab_id(*, user, pool_queryset):
    return QuizService.pick_random_vocab(user=user, queryset=pool_queryset)

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
    question_pool_qs, fallback_used = get_question_pool(request=request)

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

    user_vocab_id = get_target_user_vocab_id(user=request.user, pool_queryset=question_pool_qs)

    if user_vocab_id is None:
        return {
            "main_html": render_to_string(
                "quiz/partials/quiz_no_question_partial.html",
                request=request,
            ),
            "input_panel_html": "",
        }

    quiz_session = request.session["quiz_session"]
    quiz_session["question_user_vocab_id"] = user_vocab_id
    quiz_session["fallback_used"] = fallback_used
    quiz_session["quizzed_count"] += 1
    request.session["quiz_session"] = quiz_session

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

class QuizSessionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("quiz_session"):
            return redirect("quiz:quiz_setting")
        return super().dispatch(request, *args, **kwargs)

class QuizHomeView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/quiz_home.html"

class QuizSettingView(LoginRequiredMixin, FormView):
    template_name = "quiz/quiz_setting.html"
    form_class = QuizSettingForm

    def get(self, request, *args, **kwargs):
        quiz_session = self.request.session.get("quiz_session", {})
        unfinished_question_user_vocab_id = quiz_session.get("question_user_vocab_id")
        #last_series_quiz_status = quiz_session.get("is_series_done")
        if unfinished_question_user_vocab_id:# or last_series_quiz_status:
            return redirect("quiz:quiz_unfinished")

        in_use_count = UserVocab.objects.filter(user=request.user, in_use=True).count()

        min_count = QUIZ_CONFIG["pool"]["min_in_use"]
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
            quiz_settings = self.request.session.get("quiz_settings")
            level=quiz_settings["level"]
            vocab_type=quiz_settings["vocab_type"]
            categories=quiz_settings["categories"]
            
        self.request.session["quiz_settings"] = {
            "level": level,
            "vocab_type": vocab_type,
            "categories": categories,
        }
        return redirect("quiz:quiz_play")
    
class QuizPlayView(LoginRequiredMixin, QuizSettingRequiredMixin, TemplateView):
    template_name = "quiz/quiz_play.html"

    def get(self, request, *args, **kwargs):
        question_pool_qs, fallback_used = get_question_pool(request=self.request)
        user_vocab_id = get_target_user_vocab_id(user=self.request.user, pool_queryset=question_pool_qs)
        if user_vocab_id is None:
            messages.warning(
                request,
                "No active vocab is available for this quiz. Please enable vocab items first."
            )
            return redirect("dictionary:user_vocab_list")
        
        self.request.session["quiz_session"] = {
            "aims_quiz_num": -1,
            "quizzed_count":1,
            "correct_count":0,
            "wrong_count":0,
            "skipped_count":0,
            "total_tips_count":0,
            "question_user_vocab_id": user_vocab_id,
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

class QuizSubmitAnswerView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, FormView):
    form_class = QuizForm

    def form_valid(self, form):
        question_vocab = get_object_or_404(
            UserVocab, 
            pk=form.cleaned_data.get("user_vocab_id"), 
            user=self.request.user
        )        
        quiz_session = self.request.session.get("quiz_session",{})
        fallback_used = quiz_session.get("fallback_used",False)
        is_correct = False
        if True: # question_vocab.vocab.type == VocabType.VOCAB:
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
        quiz_session["question_user_vocab_id"] = None
        quiz_session["total_tips_count"] += form.cleaned_data.get("tips_count")
        if is_correct:
            quiz_session["correct_count"] += 1
        else:
            quiz_session["wrong_count"] += 1
        self.request.session["quiz_session"] = quiz_session
        return JsonResponse({
                    "main_html": main_html,
                    "input_panel_html": "",
                })

class QuizNextView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, FormView):
    form_class = QuizNextForm

    def form_valid(self, form):
        payload = build_next_question_payload(request=self.request)
        return JsonResponse(payload)

class QuizSkipView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, FormView):
    form_class = QuizSkipForm

    def form_valid(self, form):
        quiz_session = self.request.session.get("quiz_session")
        skipped_question_vocab = quiz_session["question_user_vocab_id"]
        if skipped_question_vocab is not None:
            QuizService.skip_question_punish(user=self.request.user, user_vocab_id=skipped_question_vocab)
            quiz_session["question_user_vocab_id"] = None
            quiz_session["skipped_count"] += 1
            self.request.session["quiz_session"] = quiz_session
        
        payload = build_next_question_payload(request=self.request)
        return JsonResponse(payload)

class QuizUnfinishedView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, TemplateView):
    template_name = "quiz/quiz_play.html"

    def get(self, request, *args, **kwargs):
        quiz_session = self.request.session.get("quiz_session", {})
        unfinished_question_user_vocab_id = quiz_session.get("question_user_vocab_id")
        if unfinished_question_user_vocab_id:
            user_vocab_id = unfinished_question_user_vocab_id
            fallback_used = quiz_session.get("fallback_used")
            messages.warning(
                request,
                "You have a unanswer yet question!"
            )
        else:
            question_pool_qs, fallback_used = get_question_pool(request=self.request)
            user_vocab_id = get_target_user_vocab_id(user=self.request.user, pool_queryset=question_pool_qs)
            quiz_session["quizzed_count"] += 1
        if user_vocab_id is None:
            messages.warning(
                request,
                "No active vocab is available for this quiz. Please enable vocab items first."
            )
            return redirect("dictionary:user_vocab_list")
        
        
        quiz_session["question_user_vocab_id"] = user_vocab_id
        quiz_session["fallback_used"] = fallback_used
        request.session["quiz_session"] = quiz_session
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

class QuizSummaryView(LoginRequiredMixin, QuizSettingRequiredMixin, TemplateView):
    pass
