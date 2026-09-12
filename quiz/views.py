import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse

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
)

from dictionary.models import (
    UserVocab,
    VocabType,
)

from .service.quiz import QuizService
from .helper import (
    get_question_pool,
    get_target_user_vocab_id,
    get_input_panel_rows,
    build_next_question_payload,
    build_quiz_summary_payload,
    render_quiz_question_payload_html,
    handle_insufficient_pool,
)
logger = logging.getLogger(__name__)

from core.service.core import load_json

QUIZ_CONFIG = load_json(path="quiz/config/quiz_config.json")

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

class QuizAjaxFormMixin:
    def form_invalid(self, form):
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status = 400,
        )


class QuizHomeView(LoginRequiredMixin, TemplateView):
    template_name = "quiz/quiz_home.html"

class QuizSettingView(LoginRequiredMixin, FormView):
    template_name = "quiz/quiz_setting.html"
    form_class = QuizSettingForm

    def get(self, request, *args, **kwargs):
        quiz_session = self.request.session.get("quiz_session", None)
        if quiz_session is not None:
            unfinished_question_user_vocab_id = quiz_session.get("question_user_vocab_id")
            last_aims_quiz_num = quiz_session.get("aims_quiz_num", -1)
            last_quizzed_count = quiz_session.get("quizzed_count", 0)
            if unfinished_question_user_vocab_id:
                logger.info(
                    "Quiz setting redirected to an unanswered question: "
                    "operation=%s user_id=%s reason=%s",
                    "quiz_setting",
                    self.request.user.pk,
                    "unfinished_question",
                )
                return redirect("quiz:quiz_unfinished")
            if last_aims_quiz_num > 0 and last_aims_quiz_num > last_quizzed_count:
                logger.info(
                    "Quiz setting resumed an unfinished quiz session: "
                    "operation=%s user_id=%s reason=%s",
                    "quiz_setting",
                    self.request.user.pk,
                    "unfinished_quiz_session",
                )
                return redirect("quiz:quiz_unfinished")
            if last_aims_quiz_num > 0 and last_aims_quiz_num <= last_quizzed_count:
                self.request.session.pop("quiz_session", None)
        if handle_insufficient_pool(request=request,
                                    min_count=QUIZ_CONFIG["pool"]["min_in_use"],
                                    logger=logger,
                                    operation="quiz_setting"):
            return redirect("dictionary:user_vocab_list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        quiz_num = form.cleaned_data["quiz_num"]
        level = form.cleaned_data["level"]
        vocab_type = form.cleaned_data["vocab_type"]
        categories = list(form.cleaned_data["categories"].values_list("id", flat=True))
        if form.cleaned_data["use_last_setting"] == True:
            quiz_settings = self.request.session.get("quiz_settings")
            if quiz_settings is None:
                form.add_error("use_last_setting", "前回のクイズ設定が見つかりません。")
                return self.form_invalid(form)
            quiz_num=quiz_settings["quiz_num"]
            level=quiz_settings["level"]
            vocab_type=quiz_settings["vocab_type"]
            categories=quiz_settings["categories"]

        self.request.session["quiz_settings"] = {
            "quiz_num": quiz_num,
            "level": level,
            "vocab_type": vocab_type,
            "categories": categories,
        }
        logger.info(
            "Quiz settings saved: "
            "operation=%s user_id=%s quiz_num=%s level=%s vocab_type=%s categories=%s",
            "quiz_setting",
            self.request.user.pk,
            quiz_num,
            level,
            vocab_type,
            categories,
        )
        return redirect("quiz:quiz_play")

class QuizNoPoolConfirmView(LoginRequiredMixin, QuizSettingRequiredMixin, TemplateView):
    template_name = "quiz/quiz_no_pool_confirm.html"

    def post(self, request, *args, **kwargs):
        quiz_settings = self.request.session.get("quiz_settings")
        quiz_settings["use_full_pool"] = True
        self.request.session["quiz_settings"] = quiz_settings
        return redirect("quiz:quiz_play")

class QuizPlayView(LoginRequiredMixin, QuizSettingRequiredMixin, TemplateView):
    template_name = "quiz/quiz_play.html"

    def get(self, request, *args, **kwargs):
        question_pool_qs = get_question_pool(request=self.request)
        if not question_pool_qs.exists():
            if handle_insufficient_pool(request=request,
                                        min_count=QUIZ_CONFIG["pool"]["min_in_use"],
                                        logger=logger,
                                        operation="quiz_play"):
                return redirect("dictionary:user_vocab_list")
            messages.warning(
                request,
                "出題できる単語がありません。"
            )
            return redirect("quiz:quiz_no_pool_confirm")
        user_vocab_id = get_target_user_vocab_id(user=self.request.user, pool_queryset=question_pool_qs)
        if user_vocab_id is None:
            logger.info(
                "Quiz start rejected: "
                "operation=%s user_id=%s reason=%s",
                "quiz_play",
                self.request.user.pk,
                "no_matching_question",
            )
            messages.warning(
                request,
                "出題できる単語がありません。マイ単語帳で単語を出題対象に設定してください。"
            )
            return redirect("dictionary:user_vocab_list")

        self.request.session["quiz_session"] = {
            "aims_quiz_num": self.request.session["quiz_settings"].get("quiz_num", -1),
            "quizzed_count":1,
            "correct_count":0,
            "wrong_count":0,
            "skipped_count":0,
            "total_tips_count":0,
            "question_user_vocab_id": user_vocab_id,
        }
        self.question_vocab = get_object_or_404(UserVocab, pk=user_vocab_id, user=self.request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyboard_rows, mc_rows = get_input_panel_rows(question_vocab = self.question_vocab)
        context["current_quiz_num"] = self.request.session["quiz_session"].get("quizzed_count", 1)
        context["total_quiz_num"] = self.request.session["quiz_session"].get("aims_quiz_num", -1)
        context["question_vocab"] = self.question_vocab
        context["keyboard_rows"] = keyboard_rows
        context["mc_rows"] = mc_rows
        return context

class QuizSubmitAnswerView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, QuizAjaxFormMixin, FormView):
    form_class = QuizForm

    def form_valid(self, form):
        quiz_session = self.request.session.get("quiz_session",{})
        posted_quiz_user_vocab_id = form.cleaned_data.get("user_vocab_id")
        session_question_user_vocab_id = quiz_session.get("question_user_vocab_id")
        if posted_quiz_user_vocab_id != session_question_user_vocab_id:
            logger.info(
                "Quiz answer ignored: "
                "operation=%s user_id=%s posted_quiz_user_vocab_id=%s session_question_user_vocab_id=%s reason=%s",
                "quiz_submit_answer",
                self.request.user.pk,
                posted_quiz_user_vocab_id,
                session_question_user_vocab_id,
                "stale_or_duplicate_submission",
            )
            if session_question_user_vocab_id is None:
                main_html = render_to_string(
                    "quiz/partials/quiz_no_question_partial.html",
                    request=self.request,
                )
                return JsonResponse({
                    "success": True,
                    "main_html": main_html,
                    "input_panel_html": "",
                })
            target_vocab = (
                UserVocab.objects
                .filter(
                    pk=session_question_user_vocab_id,
                    user=self.request.user,
                    in_use=True,
                    vocab__is_active=True,
                ).select_related("vocab").first()
            )
            if target_vocab is None:
                payload = build_quiz_summary_payload(
                    request=self.request,
                    end_reason="question_unavailable",
                    ended_early=True,
                )
                return JsonResponse(payload)

            main_html, input_panel_html = render_quiz_question_payload_html(
                request=self.request,
                target_vocab=target_vocab,
            )

            return JsonResponse({
                "success": True,
                "main_html": main_html,
                "input_panel_html": input_panel_html,
            })

        question_vocab = (
            UserVocab.objects
            .filter(
                pk=form.cleaned_data.get("user_vocab_id"),
                user=self.request.user,
                in_use=True,
                vocab__is_active=True,
            ).select_related("vocab").first()
        )
        if question_vocab is None:
            payload = build_quiz_summary_payload(
                request=self.request,
                end_reason="question_unavailable",
                ended_early=True
            )
            logger.info(
                "Quiz resume stopped: "
                "operation=%s user_id=%s reason=%s",
                "quiz_submit_answer",
                self.request.user.pk,
                "no_matching_question",
            )
            return JsonResponse(payload)
        else:
            is_correct = False
            if True: # question_vocab.vocab.type == VocabType.VOCAB:
                is_correct = QuizService.check_kana_answer(
                    question_vocab=question_vocab,
                    answer=form.cleaned_data.get("answer"),
                    tips_count=form.cleaned_data.get("tips_count"),
                )
            logger.info(
                "Quiz answer checked: "
                "operation=%s user_id=%s question_user_vocab_id=%s user_answer=%s is_correct=%s",
                "quiz_submit_answer",
                self.request.user.pk,
                question_vocab.pk,
                form.cleaned_data.get("answer"),
                is_correct,
            )

            if question_vocab.vocab.type == VocabType.VOCAB or question_vocab.vocab.type == VocabType.KATAKANA:
                compared_data = QuizService.compare_kana_answer(
                                    correct_answer=question_vocab.vocab.kana,
                                    user_answer=form.cleaned_data.get("answer")
                                )
                compared_result = QuizService.gen_answer_image(compared_result=compared_data)
            else:
                compared_result = None
            main_html = render_to_string(
                "quiz/partials/quiz_result_partial.html",
                context={
                    "current_quiz_num": quiz_session["quizzed_count"],
                    "total_quiz_num": quiz_session["aims_quiz_num"],
                    "question_vocab": question_vocab,
                    "is_correct": is_correct,
                    "compared_result": compared_result,
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
                        "success": True,
                        "main_html": main_html,
                        "input_panel_html": "",
                    })

class QuizNextView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        payload = build_next_question_payload(request=self.request)
        if payload.get("quiz_ended"):
            summary_payload = build_quiz_summary_payload(
                request=self.request,
                end_reason="no_question_pool",
                ended_early=True,
            )
            return JsonResponse(summary_payload)
        return JsonResponse(payload)

class QuizSkipView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quiz_session = self.request.session.get("quiz_session")
        skipped_question_vocab_id  = quiz_session["question_user_vocab_id"]
        if skipped_question_vocab_id  is not None:
            skip_succeeded = QuizService.skip_question_punish(user=self.request.user, user_vocab_id=skipped_question_vocab_id)
            if not skip_succeeded:
                summary_payload = build_quiz_summary_payload(
                    request=self.request,
                    end_reason="question_unavailable",
                    ended_early=True,
                )
                return JsonResponse(summary_payload)
            quiz_session["question_user_vocab_id"] = None
            quiz_session["skipped_count"] += 1
            self.request.session["quiz_session"] = quiz_session
            logger.info(
                "Quiz question skipped: "
                "operation=%s user_id=%s skipped_user_vocab_id=%s",
                "quiz_skip",
                self.request.user.pk,
                skipped_question_vocab_id ,
            )

        payload = build_next_question_payload(request=self.request, is_skip=True)
        if payload.get("quiz_ended"):
            summary_payload = build_quiz_summary_payload(
                    request=self.request,
                    end_reason="no_question_pool",
                    ended_early=True,
                )
            return JsonResponse(summary_payload)
        return JsonResponse(payload)

class QuizUnfinishedView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, TemplateView):
    template_name = "quiz/quiz_play.html"

    def get(self, request, *args, **kwargs):
        quiz_session = self.request.session.get("quiz_session", {})
        unfinished_question_user_vocab_id = quiz_session.get("question_user_vocab_id")
        unfinished_question_user_vocab = None
        if unfinished_question_user_vocab_id is not None:
            unfinished_question_user_vocab = (
                UserVocab.objects
                .filter(
                    user=request.user,
                    pk=unfinished_question_user_vocab_id,
                    in_use=True,
                    vocab__is_active=True,
                ).select_related("vocab").first()
            )
            if unfinished_question_user_vocab is None:
                request.session.pop("quiz_session", None)
                messages.warning(
                    request,
                    "現在の問題が出題対象から外れたため、クイズを終了しました。"
                )
                return redirect("quiz:quiz_setting")

            self.question_vocab = unfinished_question_user_vocab
            user_vocab_id = unfinished_question_user_vocab.pk
            messages.warning(
                request,
                "まだ回答していない問題があります。"
            )
        else:
            question_pool_qs = get_question_pool(request=self.request)
            user_vocab_id = get_target_user_vocab_id(
                user=self.request.user,
                pool_queryset=question_pool_qs
            )

            if user_vocab_id is None:
                self.request.session.pop("quiz_session", None)
                logger.info(
                    "Quiz resume stopped: "
                    "operation=%s user_id=%s reason=%s",
                    "quiz_resume",
                    self.request.user.pk,
                    "no_matching_question",
                )
                messages.warning(
                    request,
                    "出題できる問題がないため、クイズを終了しました。"
                )
                return redirect("quiz:quiz_setting")

            self.question_vocab = get_object_or_404(question_pool_qs, pk=user_vocab_id, user=self.request.user)

            if unfinished_question_user_vocab_id is None:
                quiz_session["quizzed_count"] += 1

        quiz_session["question_user_vocab_id"] = self.question_vocab.pk
        request.session["quiz_session"] = quiz_session
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyboard_rows, mc_rows = get_input_panel_rows(question_vocab = self.question_vocab)

        quiz_session = self.request.session.get("quiz_session", {})
        context["current_quiz_num"] = quiz_session["quizzed_count"]
        context["total_quiz_num"] = quiz_session["aims_quiz_num"]
        context["question_vocab"] = self.question_vocab
        context["keyboard_rows"] = keyboard_rows
        context["mc_rows"] = mc_rows
        return context

class QuizSummaryView(LoginRequiredMixin, QuizSettingRequiredMixin, QuizSessionRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quiz_session = self.request.session.get("quiz_session",{})
        payload = build_quiz_summary_payload(request=self.request)
        logger.info(
            "Quiz completed: "
            "operation=%s user_id=%s quiz_count=%s target_count=%s correct_count=%s wrong_count=%s skipped_count=%s total_tips_count=%s",
            "quiz_complete",
            self.request.user.pk,
            quiz_session["quizzed_count"],
            quiz_session["aims_quiz_num"],
            quiz_session["correct_count"],
            quiz_session["wrong_count"],
            quiz_session["skipped_count"],
            quiz_session["total_tips_count"],
        )
        return JsonResponse(payload)
