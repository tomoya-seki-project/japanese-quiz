from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import (
    IntegrityError,
    close_old_connections,
    connection,
    connections,
    transaction,
)
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from dictionary.models import (
    Category,
    Vocab,
    VocabLevel,
    VocabRequest,
    VocabRequestStatus,
    VocabRequestType,
    VocabType,
)
from dictionary.service.vocab_request import VocabRequestService


class VocabRequestServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.requester = User.objects.create_user(
            email="requester@example.test",
            username="requester",
            password="test-password",
        )
        cls.reviewer = User.objects.create_superuser(
            email="reviewer@example.test",
            username="reviewer",
            password="test-password",
        )
        cls.category = Category.objects.create(
            name="animals",
            display="動物",
        )
        cls.existing_vocab = Vocab.objects.create(
            word="犬",
            kana="いぬ",
            meaning="動物",
            type=VocabType.VOCAB,
            level=VocabLevel.JLPT_N5,
            is_active=True,
        )

    def create_request(self, *, with_category=True):
        request = VocabRequest.objects.create(
            request_type=VocabRequestType.CREATE,
            status=VocabRequestStatus.PENDING,
            created_by=self.requester,
            proposed_word="猫",
            proposed_kana="ねこ",
            proposed_meaning="動物",
            proposed_vocab_type=VocabType.VOCAB,
            proposed_level=VocabLevel.JLPT_N5,
        )
        if with_category:
            request.proposed_categories.add(self.category)
        return request

    def test_approve_request_is_applied_only_once(self):
        request = self.create_request()

        first = VocabRequestService.approve_vocab_request(
            request,
            self.reviewer,
        )
        second = VocabRequestService.approve_vocab_request(
            request,
            self.reviewer,
        )

        self.assertTrue(first)
        self.assertFalse(second)
        request.refresh_from_db()
        self.assertEqual(request.status, VocabRequestStatus.APPROVED)
        self.assertEqual(request.reviewed_by, self.reviewer)
        approved = Vocab.objects.get(word="猫", kana="ねこ")
        self.assertTrue(approved.is_active)
        self.assertEqual(approved.approved_by, self.reviewer)
        self.assertEqual(
            Vocab.objects.filter(word="猫", kana="ねこ").count(),
            1,
        )

    def test_reject_request_is_applied_only_once(self):
        request = self.create_request()

        first = VocabRequestService.reject_vocab_request(
            request,
            self.reviewer,
        )
        second = VocabRequestService.reject_vocab_request(
            request,
            self.reviewer,
        )

        self.assertTrue(first)
        self.assertFalse(second)
        request.refresh_from_db()
        self.assertEqual(request.status, VocabRequestStatus.REJECTED)
        self.assertEqual(request.reviewed_by, self.reviewer)

    def test_failed_approval_rolls_back_request_status(self):
        request = self.create_request(with_category=False)

        with self.assertRaises(ValidationError):
            VocabRequestService.approve_vocab_request(
                request,
                self.reviewer,
            )

        request.refresh_from_db()
        self.assertEqual(request.status, VocabRequestStatus.PENDING)
        self.assertIsNone(request.reviewed_by)
        self.assertFalse(
            Vocab.objects.filter(word="猫", kana="ねこ").exists()
        )

    def test_database_rejects_duplicate_pending_create_request(self):
        self.create_request()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                VocabRequest.objects.create(
                    request_type=VocabRequestType.CREATE,
                    status=VocabRequestStatus.PENDING,
                    created_by=self.requester,
                    proposed_word="猫",
                    proposed_kana="ねこ",
                )

        self.assertEqual(
            VocabRequest.objects.filter(
                status=VocabRequestStatus.PENDING,
                proposed_word="猫",
                proposed_kana="ねこ",
            ).count(),
            1,
        )

    def test_request_pages_require_login_and_admin_review_requires_staff(self):
        request = self.create_request()
        protected_urls = (
            reverse("dictionary:vocab_create"),
            reverse(
                "dictionary:vocab_update",
                kwargs={"vocab_id": self.existing_vocab.pk},
            ),
            reverse(
                "dictionary:vocab_delete",
                kwargs={"vocab_id": self.existing_vocab.pk},
            ),
        )

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn(settings.LOGIN_URL, response["Location"])

        self.client.force_login(self.requester)
        admin_url = reverse(
            "admin:dictionary_vocabrequest_change",
            args=[request.pk],
        )
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 302)
        request.refresh_from_db()
        self.assertEqual(request.status, VocabRequestStatus.PENDING)


@skipUnless(
    connection.vendor == "postgresql",
    "PostgreSQL is required to verify row-lock concurrency.",
)
class VocabRequestPostgreSQLConcurrencyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        User = get_user_model()
        self.requester = User.objects.create_user(
            email="concurrent-requester@example.test",
            username="concurrent-requester",
            password="test-password",
        )
        self.reviewer = User.objects.create_superuser(
            email="concurrent-reviewer@example.test",
            username="concurrent-reviewer",
            password="test-password",
        )
        category = Category.objects.create(
            name="concurrent-animals",
            display="動物",
        )
        self.request = VocabRequest.objects.create(
            request_type=VocabRequestType.CREATE,
            status=VocabRequestStatus.PENDING,
            created_by=self.requester,
            proposed_word="兎",
            proposed_kana="うさぎ",
            proposed_meaning="動物",
            proposed_vocab_type=VocabType.VOCAB,
            proposed_level=VocabLevel.JLPT_N5,
        )
        self.request.proposed_categories.add(category)

    def test_simultaneous_approvals_create_vocab_once(self):
        barrier = Barrier(2)

        def approve():
            close_old_connections()
            try:
                barrier.wait()
                return VocabRequestService.approve_vocab_request(
                    self.request,
                    self.reviewer,
                )
            finally:
                connections["default"].close()

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: approve(), range(2)))

        self.assertCountEqual(results, [True, False])
        self.request.refresh_from_db()
        self.assertEqual(
            self.request.status,
            VocabRequestStatus.APPROVED,
        )
        self.assertEqual(
            Vocab.objects.filter(word="兎", kana="うさぎ").count(),
            1,
        )
