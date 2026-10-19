from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import close_old_connections, connection, connections
from django.test import TestCase, TransactionTestCase

from dictionary.models import UserVocab, Vocab, VocabLevel, VocabType
from quiz.models import QuizAttempt
from quiz.service.quiz import QuizService


class QuizAttemptServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="learner@example.test",
            username="learner",
            password="test-password",
        )
        cls.other_user = User.objects.create_user(
            email="other@example.test",
            username="other",
            password="test-password",
        )
        cls.vocab = Vocab.objects.create(
            word="猫",
            kana="ねこ",
            meaning="動物",
            type=VocabType.VOCAB,
            level=VocabLevel.JLPT_N5,
            is_active=True,
        )
        cls.user_vocab = UserVocab.objects.create(
            user=cls.user,
            vocab=cls.vocab,
        )

    def create_attempt(self):
        return QuizAttempt.objects.create(
            user=self.user,
            user_vocab=self.user_vocab,
        )

    def test_only_attempt_owner_can_process_answer(self):
        attempt = self.create_attempt()

        success, error, result, user_vocab = (
            QuizService.process_answer_attempt(
                user=self.other_user,
                attempt_token=attempt.token,
                answer="ねこ",
            )
        )

        self.assertFalse(success)
        self.assertEqual(error, "attempt_not_found")
        self.assertIsNone(result)
        self.assertIsNone(user_vocab)
        attempt.refresh_from_db()
        self.user_vocab.refresh_from_db()
        self.assertEqual(attempt.status, QuizAttempt.Status.PENDING)
        self.assertEqual(self.user_vocab.correct_count, 0)

    def test_answer_attempt_is_processed_only_once(self):
        attempt = self.create_attempt()

        first = QuizService.process_answer_attempt(
            user=self.user,
            attempt_token=attempt.token,
            answer="ねこ",
        )
        second = QuizService.process_answer_attempt(
            user=self.user,
            attempt_token=attempt.token,
            answer="ねこ",
        )

        self.assertEqual(first[0:2], (True, None))
        self.assertEqual(second[0:2], (False, "already_processed"))
        attempt.refresh_from_db()
        self.user_vocab.refresh_from_db()
        self.assertEqual(attempt.status, QuizAttempt.Status.ANSWERED)
        self.assertIsNotNone(attempt.processed_at)
        self.assertEqual(self.user_vocab.correct_count, 1)

    def test_skip_attempt_is_processed_only_once(self):
        attempt = self.create_attempt()
        initial_weight = self.user_vocab.weight

        first = QuizService.process_skip_attempt(
            user=self.user,
            attempt_token=attempt.token,
        )
        second = QuizService.process_skip_attempt(
            user=self.user,
            attempt_token=attempt.token,
        )

        self.assertEqual(first, (True, None))
        self.assertEqual(second, (False, "already_processed"))
        attempt.refresh_from_db()
        self.user_vocab.refresh_from_db()
        self.assertEqual(attempt.status, QuizAttempt.Status.SKIPPED)
        self.assertIsNotNone(attempt.processed_at)
        self.assertEqual(self.user_vocab.weight, initial_weight + 50)
        self.assertEqual(self.user_vocab.streak, -1)

    def test_unavailable_question_keeps_attempt_pending(self):
        attempt = self.create_attempt()
        self.vocab.is_active = False
        self.vocab.save(update_fields=["is_active"])

        success, error, result, user_vocab = (
            QuizService.process_answer_attempt(
                user=self.user,
                attempt_token=attempt.token,
                answer="ねこ",
            )
        )

        self.assertFalse(success)
        self.assertEqual(error, "question_unavailable")
        self.assertIsNone(result)
        self.assertIsNone(user_vocab)
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, QuizAttempt.Status.PENDING)
        self.assertIsNone(attempt.processed_at)

    def test_create_attempt_rejects_another_users_vocab(self):
        with self.assertRaisesMessage(
            ValidationError,
            "The selected question is no longer available.",
        ):
            QuizService.create_quiz_attempt(
                user=self.other_user,
                user_vocab_id=self.user_vocab.pk,
            )

        self.assertFalse(
            QuizAttempt.objects.filter(user=self.other_user).exists()
        )


@skipUnless(
    connection.vendor == "postgresql",
    "PostgreSQL is required to verify row-lock concurrency.",
)
class QuizAttemptPostgreSQLConcurrencyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="concurrent@example.test",
            username="concurrent",
            password="test-password",
        )
        vocab = Vocab.objects.create(
            word="鳥",
            kana="とり",
            meaning="動物",
            type=VocabType.VOCAB,
            level=VocabLevel.JLPT_N5,
            is_active=True,
        )
        self.user_vocab = UserVocab.objects.create(
            user=self.user,
            vocab=vocab,
        )
        self.attempt = QuizAttempt.objects.create(
            user=self.user,
            user_vocab=self.user_vocab,
        )

    def test_simultaneous_answers_apply_result_once(self):
        barrier = Barrier(2)

        def answer():
            close_old_connections()
            try:
                barrier.wait()
                return QuizService.process_answer_attempt(
                    user=self.user,
                    attempt_token=self.attempt.token,
                    answer="とり",
                )
            finally:
                connections["default"].close()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: answer(), range(2)))

        self.assertCountEqual(
            [result[0:2] for result in results],
            [(True, None), (False, "already_processed")],
        )
        self.attempt.refresh_from_db()
        self.user_vocab.refresh_from_db()
        self.assertEqual(self.attempt.status, QuizAttempt.Status.ANSWERED)
        self.assertEqual(self.user_vocab.correct_count, 1)
