
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from django.contrib import messages

from .constants import HIRAGANA_ROWS, KATAKANA_ROWS

from .service.quiz import QuizService

from dictionary.models import (
    UserVocab,
    VocabType,
)
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
    
    quiz_session = request.session["quiz_session"]
    main_html = render_to_string(
        "quiz/partials/quiz_question_partial.html",
        context={
            "current_quiz_num": quiz_session["quizzed_count"],
            "total_quiz_num": quiz_session["aims_quiz_num"],
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

def build_next_question_payload(*, request, is_skip=False):
    question_pool_qs, fallback_used = get_question_pool(request=request)

    if fallback_used:
        messages.warning(
            request,
            "条件に一致する単語がありません。今回は、出題対象に設定したすべての単語から出題します。"
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
    if is_skip is False:
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
        "success": True,
        "main_html": main_html,
        "input_panel_html": input_panel_html,
    }
