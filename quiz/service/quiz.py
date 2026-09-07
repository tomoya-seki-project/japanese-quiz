import random
from bisect import bisect_left
from django.utils import timezone

from dataclasses import dataclass
from typing import Optional

from dictionary.models import (
    Vocab,
    UserVocab,
    Category,
)

from core.service.core import load_json

QUIZ_CONFIG = load_json(path="quiz/config/quiz_config.json")
COMPARE_SUBTYPE = load_json(path="quiz/config/compare_answer_subtype.json")
KANA_GRAPHIC_MAP = load_json(path="quiz/config/kana_graphic_map.json")

@dataclass
class Score:
    cost: int
    match_count: int
    non_normal_wrong_count: int

@dataclass
class DPCell:
    score: Score
    operation: Optional[str]
    sub_operation: str | None = None

class QuizService():
    @staticmethod
    def create_question_pool(*, user, vocab_type=None, level=None, categories=None, use_full_pool=False):
        full_qs = UserVocab.objects.filter(user=user, in_use=True, vocab__is_active=True).select_related("vocab").distinct()

        filtered_qs = full_qs

        if not use_full_pool:
            if vocab_type:
                filtered_qs = filtered_qs.filter(vocab__type__in=vocab_type)
            if level:
                filtered_qs = filtered_qs.filter(vocab__level__in=level)
            if categories:
                filtered_qs = filtered_qs.filter(vocab__categories__in=categories).distinct()

            if filtered_qs.count() > QUIZ_CONFIG["pool"]["min_in_use"]:
                recently_quizzed_ids = (
                    filtered_qs.filter(last_quiz_at__isnull=False)
                    .order_by("-last_quiz_at")
                    .values_list("id", flat=True)[:QUIZ_CONFIG["pool"]["min_in_use"]]
                )
                filtered_qs = filtered_qs.exclude(id__in=recently_quizzed_ids)

        return filtered_qs

    @staticmethod
    def pick_random_vocab(*, user, queryset=None):
        if queryset is None:
            queryset = QuizService.create_question_pool(user=user)

        weight_rows = list(queryset.values_list("id", "weight"))

        if not weight_rows:
            return None

        total_weight = 0
        cumulative_weight = []

        for user_vocab_id, weight in weight_rows:
            total_weight += weight
            cumulative_weight.append(total_weight)

        # Normally every vocab should have at least 1 weight, so total_weight should not be 0.
        if total_weight <= 0:
            return None

        random_number = random.randint(1, total_weight)

        index = bisect_left(
            cumulative_weight,
            random_number,
        )

        return weight_rows[index][0]

    @staticmethod
    def skip_question_punish(*, user, user_vocab_id):
        skipped_user_vocab = UserVocab.objects.filter(pk=user_vocab_id, user=user).first()
        if skipped_user_vocab is not None:
            skipped_user_vocab.weight += QUIZ_CONFIG["weight"]["skip"]
            if skipped_user_vocab.streak > 0:
                skipped_user_vocab.streak = 0
            else:
                skipped_user_vocab.streak -= 1
            skipped_user_vocab.last_quiz_at = timezone.now()
            skipped_user_vocab.save(
                update_fields=["weight","streak","last_quiz_at"]
            )

    @staticmethod
    def check_kana_answer(*, question_vocab=None, answer=None, tips_count=0):
        is_correct = False
        if question_vocab is None:
            return -1

        if answer is None:
            return -2
        WEIGHT_CONFIG = QUIZ_CONFIG["weight"]
        tips_count = max(0, min(tips_count, 50))
        new_weight = min(WEIGHT_CONFIG["max_tips"], tips_count * WEIGHT_CONFIG["tips"])

        if question_vocab.vocab.kana == answer:
            is_correct = True
            question_vocab.correct_count += 1
            if question_vocab.streak < 0:
                question_vocab.streak = 1
            else:
                question_vocab.streak += 1
            new_weight += (WEIGHT_CONFIG["correct"] + (abs(question_vocab.streak) * WEIGHT_CONFIG["streak_correct"] ))
        else:
            is_correct = False
            question_vocab.incorrect_count += 1
            if question_vocab.streak > 0:
                question_vocab.streak = -1
            else:
                question_vocab.streak -= 1
            new_weight += (WEIGHT_CONFIG["wrong"] + (abs(question_vocab.streak) * WEIGHT_CONFIG["streak_wrong"] ))

        question_vocab.weight = max(WEIGHT_CONFIG["min_weight"], question_vocab.weight + new_weight)
        question_vocab.last_answer = answer

        question_vocab.last_quiz_at = timezone.now()
        question_vocab.save(
            update_fields=["streak", "correct_count", "incorrect_count", "weight", "last_quiz_at", "last_answer"]
        )
        return is_correct

    @staticmethod
    def check_mc_answer(*, question_vocab=None, answer=None):
        if question_vocab is None:
            return -1

        if answer is None:
            return -2

        if question_vocab.vocab.kana == answer:
            question_vocab.correct_count += 1
            if question_vocab.streak < 0:
                question_vocab.streak = 1
            else:
                question_vocab.streak += 1
        else:
            question_vocab.incorrect_count += 1
            if question_vocab.streak > 0:
                question_vocab.streak = -1
            else:
                question_vocab.streak -= 1

        question_vocab.last_answer = answer

        question_vocab.last_quiz_at = timezone.now()
        question_vocab.save(
            update_fields=["streak", "correct_count", "incorrect_count", "weight", "last_quiz_at", "last_answer"]
        )



    @staticmethod
    def gen_answer_image(*, compared_result):
        answer_graphic = []
        for letter_result in compared_result["result"]:
            if letter_result["type"] == "WRONG":
                kana_config = KANA_GRAPHIC_MAP.get(letter_result["correct"], {})
                type_config = kana_config.get(letter_result["type"], {})
                subtype_config = type_config.get(letter_result["sub_type"], type_config.get("NORMAL", {}))
                answer_graphic.append(
                    {
                        "type": letter_result["type"],
                        "sub_type": letter_result["sub_type"],
                        "correct": letter_result["correct"],
                        "answer": letter_result["answer"],
                        "image_path": subtype_config.get("image_path"),
                        "sub_image_path": subtype_config.get("sub_image_path", ""),
                        "font_width": subtype_config.get("font_width", 500)
                    }
                )

            elif letter_result["type"] in ["MATCH", "MISSING"]:
                kana_config = KANA_GRAPHIC_MAP.get(letter_result["correct"], {})
                type_config = kana_config.get(letter_result["type"], {})
                answer_graphic.append(
                    {
                        "type": letter_result["type"],
                        "sub_type": letter_result["sub_type"],
                        "correct": letter_result["correct"],
                        "answer": letter_result["answer"],
                        "image_path": type_config.get("image_path"),
                        "sub_image_path": type_config.get("sub_image_path", ""),
                        "font_width": type_config.get("font_width", 500)
                    }
                )
            else:
                kana_config = KANA_GRAPHIC_MAP.get(letter_result["answer"], {})
                type_config = kana_config.get(letter_result["type"], {})
                answer_graphic.append(
                    {
                        "type": letter_result["type"],
                        "sub_type": letter_result["sub_type"],
                        "correct": letter_result["correct"],
                        "answer": letter_result["answer"],
                        "image_path": type_config.get("image_path"),
                        "sub_image_path": type_config.get("sub_image_path", ""),
                        "font_width": type_config.get("font_width", 500)
                    }
                )
        return answer_graphic

    @staticmethod
    def compare_kana_answer(*, correct_answer, user_answer):
        return QuizService.answer_compare_dp(
            correct_answer=correct_answer or "",
            user_answer=user_answer or ""
        )

    @staticmethod
    def define_wrong_sub_type(*, correct_letter, user_letter):
        subtype = COMPARE_SUBTYPE.get(correct_letter, {}).get(user_letter)
        return subtype if subtype is not None else "NORMAL"

    @staticmethod
    def answer_compare_dp(*, correct_answer, user_answer):
        m = len(correct_answer)
        n = len(user_answer)
        dp_table : list[list[Optional[DPCell]]] = [
            [None for _ in range(n + 1)]
            for _ in range(m + 1)
        ]

        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i == m and j == n:
                    dp_table[i][j] = DPCell(
                        score=Score(
                            cost=0,
                            match_count=0,
                            non_normal_wrong_count=0,
                        ),
                        operation="END"
                    )
                elif i == m:
                    next_cell = dp_table[i][j+1]
                    dp_table[i][j] = DPCell(
                        score=Score(
                            cost=next_cell.score.cost + 1,
                            match_count=next_cell.score.match_count,
                            non_normal_wrong_count=next_cell.score.non_normal_wrong_count,
                        ),
                        operation="EXTRA"
                    )
                elif j == n:
                    next_cell = dp_table[i+1][j]
                    dp_table[i][j] = DPCell(
                        score=Score(
                            cost=next_cell.score.cost + 1,
                            match_count=next_cell.score.match_count,
                            non_normal_wrong_count=next_cell.score.non_normal_wrong_count,
                        ),
                        operation="MISSING"
                    )
                else:
                    # match section
                    if correct_answer[i] == user_answer[j]:
                        next_cell = dp_table[i+1][j+1]
                        dp_table[i][j] = DPCell(
                            score=Score(
                                cost=next_cell.score.cost,
                                match_count=next_cell.score.match_count + 1,
                                non_normal_wrong_count=next_cell.score.non_normal_wrong_count,
                            ),
                            operation="MATCH"
                        )
                    else:
                        # wrong section
                        next_wrong_cell = dp_table[i+1][j+1]
                        sub_operation = QuizService.define_wrong_sub_type(
                            correct_letter=correct_answer[i],
                            user_letter=user_answer[j]
                        )
                        wrong_result = DPCell(
                            score=Score(
                                cost=next_wrong_cell.score.cost + 1,
                                match_count=next_wrong_cell.score.match_count,
                                non_normal_wrong_count=
                                        next_wrong_cell.score.non_normal_wrong_count
                                        + (1 if sub_operation != "NORMAL" else 0)
                            ),
                            operation="WRONG",
                            sub_operation=sub_operation
                        )
                        # missing section
                        next_missing_cell = dp_table[i+1][j]
                        missing_result = DPCell(
                            score=Score(
                                cost=next_missing_cell.score.cost + 1,
                                match_count=next_missing_cell.score.match_count,
                                non_normal_wrong_count=next_missing_cell.score.non_normal_wrong_count,
                            ),
                            operation="MISSING"
                        )
                        # extra section
                        next_extra_cell = dp_table[i][j+1]
                        extra_result = DPCell(
                            score=Score(
                                cost=next_extra_cell.score.cost + 1,
                                match_count=next_extra_cell.score.match_count,
                                non_normal_wrong_count=next_extra_cell.score.non_normal_wrong_count,
                            ),
                            operation="EXTRA"
                        )
                        dp_table[i][j] = min(
                            wrong_result,
                            missing_result,
                            extra_result,
                            key=lambda result: (
                                result.score.cost,
                                -result.score.match_count,
                                -result.score.non_normal_wrong_count,
                            )
                        )
        result = []
        result_i = 0
        result_j = 0
        while dp_table[result_i][result_j].operation != "END":
            cell = dp_table[result_i][result_j]
            match cell.operation:
                case "MATCH":
                    result.append({
                        "type": "MATCH",
                        "sub_type": None,
                        "correct": correct_answer[result_i],
                        "answer": user_answer[result_j],
                    })
                    result_i += 1
                    result_j += 1
                case "WRONG":
                    result.append({
                        "type": "WRONG",
                        "sub_type": cell.sub_operation,
                        "correct": correct_answer[result_i],
                        "answer": user_answer[result_j],
                    })
                    result_i += 1
                    result_j += 1
                case "MISSING":
                    result.append({
                        "type": "MISSING",
                        "sub_type": None,
                        "correct": correct_answer[result_i],
                        "answer": None,
                    })
                    result_i += 1
                case "EXTRA":
                    result.append({
                        "type": "EXTRA",
                        "sub_type": None,
                        "correct": None,
                        "answer": user_answer[result_j],
                    })
                    result_j += 1
                case _:
                    raise ValueError(f"Unknown operation: {cell.operation}")
        return {
            "cost": dp_table[0][0].score.cost,
            "match_count": dp_table[0][0].score.match_count,
            "non_normal_wrong_count": dp_table[0][0].score.non_normal_wrong_count,
            "result": result,
        }