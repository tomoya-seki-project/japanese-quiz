
import logging
from django.template.loader import render_to_string

from django.core.exceptions import ValidationError

from django.contrib import messages

from .constants import HIRAGANA_ROWS, KATAKANA_ROWS

from .service.quiz import QuizService

from dictionary.models import (
    UserVocab,
    VocabType,
)


logger = logging.getLogger(__name__)

def get_question_pool(*, request):
    quiz_settings = request.session.get("quiz_settings")
    question_pool_qs = QuizService.create_question_pool(
        user=request.user,
        vocab_type=quiz_settings["vocab_type"],
        level=quiz_settings["level"],
        categories=quiz_settings["categories"],
        use_full_pool=request.session.get("quiz_use_full_pool", False)
    )
    return question_pool_qs

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

def render_quiz_question_payload_html(*, request, target_vocab):
    keyboard_rows, mc_rows = get_input_panel_rows(question_vocab = target_vocab)

    quiz_session = request.session["quiz_session"]
    main_html = render_to_string(
        "quiz/partials/quiz_question_partial.html",
        context={
            "current_quiz_num": quiz_session["quizzed_count"],
            "total_quiz_num": quiz_session["aims_quiz_num"],
            "question_vocab": target_vocab,
            "question_attempt_token": quiz_session["question_attempt_token"],
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

def build_next_question_payload(*, request, is_skip=False):
    question_pool_qs = get_question_pool(request=request)

    user_vocab_id = get_target_user_vocab_id(user=request.user, pool_queryset=question_pool_qs)

    if user_vocab_id is None:
        return {
            "success": True,
            "quiz_ended": True,
        }

    try:
        quiz_attempt = QuizService.create_quiz_attempt(user=request.user, user_vocab_id=user_vocab_id)
    except ValidationError:
        logger.info(
            "Quiz start rejected becuase selected question "
            "become unavailable: operation=%s user_id=%s user_vocab_id=%s",
            "quiz_attempt_create",
            request.user.pk,
            user_vocab_id
        )
        messages.warning(
            request,
            "出題予定の単語が利用できなくなりました。"
        )
        return {
            "success": True,
            "quiz_ended": True,
        }

    quiz_session = request.session["quiz_session"]
    quiz_session["question_user_vocab_id"] = user_vocab_id
    quiz_session["question_attempt_token"] = str(quiz_attempt.token)
    if is_skip is False:
        quiz_session["quizzed_count"] += 1
    request.session["quiz_session"] = quiz_session

    target_vocab = quiz_attempt.user_vocab

    main_html, input_panel_html = render_quiz_question_payload_html(
        request=request,
        target_vocab=target_vocab,
    )

    return {
        "success": True,
        "main_html": main_html,
        "input_panel_html": input_panel_html,
    }

def build_quiz_summary_payload(*, request, end_reason="completed", ended_early=False):
    quiz_session = request.session.get("quiz_session",{})
    main_html = render_to_string(
        "quiz/partials/quiz_summary_partial.html",
        context={
            "current_quiz_num": quiz_session["quizzed_count"],
            "total_quiz_num": quiz_session["aims_quiz_num"],
            "correct_count":quiz_session["correct_count"],
            "wrong_count":quiz_session["wrong_count"],
            "skipped_count":quiz_session["skipped_count"],
            "total_tips_count":quiz_session["total_tips_count"],
            "ended_early": ended_early,
            "end_reason": end_reason,
        },
        request=request,
    )

    request.session.pop("quiz_use_full_pool", None)
    request.session.pop("quiz_session", None)
    return {
        "success":True,
        "main_html": main_html,
        "input_panel_html": "",
        "end_reason": end_reason,
        "ended_early": ended_early,
    }


def handle_insufficient_pool(*, request, min_count, logger, operation):
    in_use_count = UserVocab.objects.filter(user=request.user, in_use=True, vocab__is_active=True).count()

    if in_use_count < min_count:
        logger.info(
            "Quiz start rejected due to insufficient active vocab: "
            "operation=%s user_id=%s required_count=%s in_use_count=%s",
            operation,
            request.user.pk,
            min_count,
            in_use_count,
        )
        messages.warning(
            request,
            f"クイズを始めるには、出題対象の単語が{min_count}語以上必要です。マイ単語帳で出題対象を追加してください。"
        )
        return True
    return False