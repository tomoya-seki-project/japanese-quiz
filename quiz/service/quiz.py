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
        qs = UserVocab.objects.filter(user=user, in_use=True).select_related("vocab").distinct()

        if vocab_type is not None:
            qs = qs.filter(vocab__type__in=vocab_type)
        if level is not None:
            qs = qs.filter(vocab__level__in=level)
        if categories is not None:
            qs = qs.filter(vocab__categories__in=categories).distinct()

        qs = qs.order_by("-last_quiz_at")[10:]

        return qs
    
    @staticmethod
    def pick_random_vocab(*, user, queryset=None):
        if queryset is None:
            queryset = QuizService.create_question_pool(user=user)

        vocab_list = list(queryset)
        total_weight = 0
        cumulative_weight = []

        for user_vocab in vocab_list:
            total_weight += user_vocab.weight
            cumulative_weight.append(total_weight)

        # normally since all of vocab will have atleast 1 weight, total_weight not possible be 0 
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

        question_vocab.last_quiz_at = timezone.now()
        question_vocab.save(
            update_fields=["streak", "correct_count", "incorrect_count", "weight", "last_quiz_at"]
        )

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
        question_vocab.last_quiz_at = timezone.now()
        question_vocab.save(
            update_fields=["streak", "correct_count", "incorrect_count", "weight", "last_quiz_at"]
        )