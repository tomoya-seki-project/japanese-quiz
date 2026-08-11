import random
from bisect import bisect_left
from django.utils import timezone

from dictionary.models import (
    Vocab,
    UserVocab,
    Category,
)

from core.service.core import load_json

QUIZ_CONFIG = load_json(path="quiz/config/quiz_config.json")
COMPARE_SUBTYPE = load_json(path="quiz/config/compare_answer_subtype.json")
KANA_GRAPHIC_MAP = load_json(path="quiz/config/kana_graphic_map.json")

class QuizService():
    @staticmethod
    def create_question_pool(*, user, vocab_type=None, level=None, categories=None):
        full_qs = UserVocab.objects.filter(user=user, in_use=True, vocab__is_active=True).select_related("vocab").distinct()

        filtered_qs = full_qs

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

        fallback_used = False
        if not filtered_qs.exists():
            output_qs = full_qs
            fallback_used = True
        else:
            output_qs = filtered_qs

        return output_qs, fallback_used
    
    @staticmethod
    def pick_random_vocab(*, user, queryset=None):
        if queryset is None:
            queryset, fallback_used = QuizService.create_question_pool(user=user)

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
                        "font_width": type_config.get("font_width", 500)
                    }
                )
        return answer_graphic

    @staticmethod
    def compare_kana_answer(*, correct_answer, user_answer):
        return QuizService.answer_compare(
            correct_answer=correct_answer or "",
            user_answer=user_answer or "",
            pos_of_correct=0,
            pos_of_user=0,
        )

    @staticmethod
    def define_wrong_sub_type(*, correct_letter, user_letter):
        subtype = COMPARE_SUBTYPE.get(correct_letter, {}).get(user_letter)
        return subtype if subtype is not None else "NORMAL"

    @staticmethod
    def answer_compare(*, correct_answer, user_answer, pos_of_correct, pos_of_user):
        if pos_of_correct >= len(correct_answer) and pos_of_user >= len(user_answer):
            return {
                "cost": 0,
                "match_count": 0,
                "non_normal_wrong_count": 0,
                "result": [],
            }
        if pos_of_correct >= len(correct_answer):
            return {
                "cost": len(user_answer) - pos_of_user,
                "match_count": 0,
                "non_normal_wrong_count": 0,
                "result": [
                    {
                        "type": "EXTRA",
                        "sub_type": None,
                        "correct": None,
                        "answer": char,
                    }
                    for char in user_answer[pos_of_user:]
                ]
            }
        if pos_of_user >= len(user_answer):
            return {
                "cost": len(correct_answer) - pos_of_correct,
                "match_count": 0,
                "non_normal_wrong_count": 0,
                "result": [
                    {
                        "type": "MISSING",
                        "sub_type": None,
                        "correct": char,
                        "answer": None,
                    }
                    for char in correct_answer[pos_of_correct:]
                ]
            }
        if correct_answer[pos_of_correct] == user_answer[pos_of_user]:
            next_compare_result = QuizService.answer_compare(
                correct_answer=correct_answer,
                user_answer=user_answer,
                pos_of_correct=pos_of_correct+1,
                pos_of_user=pos_of_user+1,
            )
            return {
                "cost": next_compare_result["cost"],
                "match_count": 1 + next_compare_result["match_count"],
                "non_normal_wrong_count": next_compare_result["non_normal_wrong_count"],
                "result": [
                    {
                        "type": "MATCH",
                        "sub_type": None,
                        "correct": correct_answer[pos_of_correct],
                        "answer": user_answer[pos_of_user],
                    },
                ] + next_compare_result["result"],
            }
        wrong_next = QuizService.answer_compare(
            correct_answer=correct_answer,
            user_answer=user_answer,
            pos_of_correct=pos_of_correct+1,
            pos_of_user=pos_of_user+1,
        )
        sub_type = QuizService.define_wrong_sub_type(
                        correct_letter=correct_answer[pos_of_correct],
                        user_letter=user_answer[pos_of_user]
                    )
        wrong = {
            "cost": 1 + wrong_next["cost"],
            "match_count": wrong_next["match_count"],
            "non_normal_wrong_count": wrong_next["non_normal_wrong_count"] + (1 if sub_type != "NORMAL" else 0),
            "result": [
                {
                    "type": "WRONG",
                    "sub_type": sub_type,
                    "correct": correct_answer[pos_of_correct],
                    "answer": user_answer[pos_of_user],
                },
            ] + wrong_next["result"],
        }

        missing_next = QuizService.answer_compare(
            correct_answer=correct_answer,
            user_answer=user_answer,
            pos_of_correct=pos_of_correct+1,
            pos_of_user=pos_of_user,
        )
        missing = {
            "cost": 1 + missing_next["cost"],
            "match_count": missing_next["match_count"],
            "non_normal_wrong_count": missing_next["non_normal_wrong_count"],
            "result": [
                {
                    "type": "MISSING",
                    "sub_type": None,
                    "correct": correct_answer[pos_of_correct],
                    "answer": None,
                },
            ] + missing_next["result"],
        }

        extra_next = QuizService.answer_compare(
            correct_answer=correct_answer,
            user_answer=user_answer,
            pos_of_correct=pos_of_correct,
            pos_of_user=pos_of_user+1,
        )
        extra = {
            "cost": 1 + extra_next["cost"],
            "match_count": extra_next["match_count"],
            "non_normal_wrong_count": extra_next["non_normal_wrong_count"],
            "result": [
                {
                    "type": "EXTRA",
                    "sub_type": None,
                    "correct": None,
                    "answer": user_answer[pos_of_user],
                },
            ] + extra_next["result"],
        }

        return min(
                wrong, 
                missing, 
                extra, 
                key=lambda result: (
                    result["cost"], 
                    -result["match_count"],
                    -result["non_normal_wrong_count"],
                )
            )
