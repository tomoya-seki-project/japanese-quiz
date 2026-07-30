import random
from bisect import bisect_left
from django.utils import timezone

from dictionary.models import (
    Vocab,
    UserVocab,
    Category,
)

class QuizService():
    @staticmethod
    def create_question_pool(*, user, vocab_type=None, level=None, categories=None):
        full_qs = UserVocab.objects.filter(user=user, in_use=True).select_related("vocab").distinct()

        filtered_qs = full_qs

        if vocab_type:
            filtered_qs = filtered_qs.filter(vocab__type__in=vocab_type)
        if level:
            filtered_qs = filtered_qs.filter(vocab__level__in=level)
        if categories:
            filtered_qs = filtered_qs.filter(vocab__categories__in=categories).distinct()

        if filtered_qs.count() > 10:
            recently_quizzed_ids = (
                filtered_qs.filter(last_quiz_at__isnull=False)
                .order_by("-last_quiz_at")
                .values_list("id", flat=True)[:10]
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

        if queryset.count() == 0:
            return None

        vocab_list = list(queryset)
        total_weight = 0
        cumulative_weight = []

        for user_vocab in vocab_list:
            total_weight += user_vocab.weight
            cumulative_weight.append(total_weight)

        # Normally every vocab should have at least 1 weight, so total_weight should not be 0.
        if total_weight <= 0:
            return None
        
        random_number = random.randint(1, total_weight)

        index = bisect_left(
            cumulative_weight,
            random_number,
        )

        return vocab_list[index].pk
    
    @staticmethod
    def check_kana_answer(*, question_vocab=None, answer=None, tips_count=0):
        is_correct = False
        if question_vocab is None:
            return -1
        
        if answer is None:
            return -2
        
        if question_vocab.vocab.kana == answer:
            is_correct = True
            question_vocab.correct_count += 1
            if question_vocab.streak < 0:
                question_vocab.streak = 1
            else:
                question_vocab.streak += 1
        else:
            is_correct = False
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

