from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import DatabaseError
from django.http import HttpResponse
from django.middleware.security import SecurityMiddleware
from django.template.loader import get_template, render_to_string
from django.test import (
    RequestFactory,
    SimpleTestCase,
    TestCase,
    override_settings,
)
from django.urls import reverse
from django.utils import translation

from accounts.forms import UserCreationAdminForm
from accounts.views import _is_ip_rate_limit_allowed
from core.forms import FeedbackCreateForm, FeedbackReplyForm
from core.models import Event, Feedback, FeedbackType
from dictionary.forms import VocabCreateRequestForm
from dictionary.models import Vocab, VocabType, VocabLevel, VocabRequest, VocabRequestStatus, VocabRequestType
from dictionary.service.vocab_request import VocabRequestService
from quiz.forms import QuizSettingForm
from config.sentry import redact_sensitive_sentry_data


@override_settings(
    CACHES={"default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "ip-rate-limit-tests",
    }},
    RATE_LIMIT_CLIENT_IP_META_KEY="HTTP_X_REAL_IP",
    REGISTRATION_IP_RATE_LIMIT=10,
    REGISTRATION_IP_RATE_LIMIT_WINDOW_SECONDS=3600,
    ACTIVATION_RESEND_IP_RATE_LIMIT=10,
    ACTIVATION_RESEND_IP_RATE_LIMIT_WINDOW_SECONDS=600,
)
class IPRateLimitTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)
        self.factory = RequestFactory()

    def allowed(self, ip="192.0.2.1", scope="registration"):
        request = self.factory.post("/", HTTP_X_REAL_IP=ip)
        return _is_ip_rate_limit_allowed(
            request=request, scope=scope, limit=10, window_seconds=600,
        )

    def test_limits_are_separate_by_ip_and_scope(self):
        for _ in range(10):
            self.assertTrue(self.allowed())
        self.assertFalse(self.allowed())
        self.assertTrue(self.allowed(ip="192.0.2.2"))
        self.assertTrue(self.allowed(scope="activation-resend"))

    def test_equivalent_ipv6_addresses_share_limit(self):
        for _ in range(10):
            self.assertTrue(self.allowed(ip="2001:db8::1"))
        self.assertFalse(self.allowed(ip="2001:0db8:0:0:0:0:0:1"))

    def test_missing_or_invalid_trusted_ip_fails_open(self):
        for value in (None, "not-an-ip", "192.0.2.1, 192.0.2.2"):
            with self.subTest(value=value):
                with self.assertLogs("accounts.views", level="ERROR"):
                    self.assertTrue(self.allowed(ip=value))

    def test_cache_failure_fails_open(self):
        with patch("accounts.views.cache.add", side_effect=RuntimeError("offline")):
            with self.assertLogs("accounts.views", level="ERROR"):
                self.assertTrue(self.allowed())

    def test_untrusted_forwarded_header_cannot_change_limit(self):
        for _ in range(10):
            self.assertTrue(self.allowed())
        request = self.factory.post(
            "/", HTTP_X_REAL_IP="192.0.2.1",
            HTTP_X_FORWARDED_FOR="192.0.2.99",
        )
        self.assertFalse(_is_ip_rate_limit_allowed(
            request=request, scope="registration", limit=10, window_seconds=600,
        ))

    def test_both_routes_block_before_creating_user_or_sending_mail(self):
        cases = (
            ("accounts:user_regist", "3600"),
            ("accounts:resend_activation_email", "600"),
        )
        for route, retry_after in cases:
            with self.subTest(route=route):
                cache.clear()
                url = reverse(route)
                for _ in range(10):
                    response = self.client.post(url, {}, HTTP_X_REAL_IP="192.0.2.1")
                    self.assertEqual(response.status_code, 200)
                user_count = get_user_model().objects.count()
                with patch("accounts.views.send_activation_email") as send:
                    response = self.client.post(url, {
                        "username": "limited-user",
                        "email": "limited@example.test",
                        "password": "test-password",
                        "password2": "test-password",
                    }, HTTP_X_REAL_IP="192.0.2.1")
                self.assertContains(response, "リクエスト回数が多すぎます。", status_code=429)
                self.assertEqual(response["Retry-After"], retry_after)
                self.assertEqual(get_user_model().objects.count(), user_count)
                send.assert_not_called()
                self.assertEqual(self.client.get(url).status_code, 200)
                self.assertEqual(self.client.post(
                    url, {}, HTTP_X_REAL_IP="192.0.2.2",
                ).status_code, 200)


class SentryDataRedactionTests(SimpleTestCase):
    def test_activation_credentials_are_redacted_recursively(self):
        event = {
            "request": {
                "url": (
                    "https://example.com/accounts/activate/"
                    "MQ/secret-token/?source=email"
                ),
            },
            "breadcrumbs": {
                "values": [
                    {
                        "message": (
                            "Opening /accounts/activate/Mg/another-token/"
                        ),
                    },
                ],
            },
            "extra": (
                "/accounts/activate/Mw/third-token/",
            ),
        }

        redacted = redact_sensitive_sentry_data(event, hint={})
        redacted_text = repr(redacted)

        self.assertEqual(
            redacted["request"]["url"],
            (
                "https://example.com/accounts/activate/"
                "[Filtered]/[Filtered]/?source=email"
            ),
        )
        self.assertNotIn("secret-token", redacted_text)
        self.assertNotIn("another-token", redacted_text)
        self.assertNotIn("third-token", redacted_text)
        self.assertNotIn("/activate/MQ/", redacted_text)
        self.assertNotIn("/activate/Mg/", redacted_text)
        self.assertNotIn("/activate/Mw/", redacted_text)

    def test_non_activation_data_is_unchanged(self):
        event = {
            "request": {
                "url": "https://example.com/accounts/user_login/",
            },
            "message": "ordinary application error",
        }

        redacted = redact_sensitive_sentry_data(event, hint={})

        self.assertEqual(redacted, event)


@override_settings(
    SECURE_PROXY_SSL_HEADER=(
        "HTTP_X_FORWARDED_PROTO",
        "https",
    ),
    SECURE_SSL_REDIRECT=True,
    ALLOWED_HOSTS=["testserver"],
)
class ProxyHTTPSSettingsTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.middleware = SecurityMiddleware(
            lambda request: HttpResponse("ok")
        )

    def test_https_proxy_header_marks_request_secure(self):
        request = self.request_factory.get(
            "/",
            HTTP_HOST="testserver",
            HTTP_X_FORWARDED_PROTO="https",
        )

        response = self.middleware(request)

        self.assertTrue(request.is_secure())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            request.build_absolute_uri("/accounts/activate/example/"),
            "https://testserver/accounts/activate/example/",
        )

    def test_missing_or_http_proxy_header_redirects_to_https(self):
        cases = (
            {},
            {"HTTP_X_FORWARDED_PROTO": "http"},
        )

        for request_meta in cases:
            with self.subTest(request_meta=request_meta):
                request = self.request_factory.get(
                    "/",
                    HTTP_HOST="testserver",
                    **request_meta,
                )

                response = self.middleware(request)

                self.assertFalse(request.is_secure())
                self.assertEqual(response.status_code, 301)
                self.assertEqual(
                    response["Location"],
                    "https://testserver/",
                )


@override_settings(
    DEBUG=False,
    SECURE_SSL_REDIRECT=True,
    ALLOWED_HOSTS=["testserver"],
)
class BadRequestHandlerTests(SimpleTestCase):
    def test_disallowed_host_returns_custom_400_page(self):
        response = self.client.get(
            "/",
            HTTP_HOST="invalid.example",
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(
            response,
            "<title>400 | 言葉の輪</title>",
            status_code=400,
            html=True,
        )


class HealthCheckTests(TestCase):
    def test_health_check_returns_ok_when_database_is_available(self):
        response = self.client.get(reverse("health"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertIn("no-store", response["Cache-Control"])

    def test_health_check_returns_503_when_database_is_unavailable(self):
        with patch(
            "core.views.connection.cursor",
            side_effect=DatabaseError("database unavailable"),
        ):
            with self.assertLogs("core.views", level="ERROR") as logs:
                response = self.client.get(
                    reverse("health"),
                    secure=True,
                )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unhealthy"})
        self.assertNotIn(b"database unavailable", response.content)
        self.assertIn("health_check_database", logs.output[0])

    def test_health_check_allows_head_but_rejects_post(self):
        head_response = self.client.head(
            reverse("health"),
            secure=True,
        )
        post_response = self.client.post(
            reverse("health"),
            secure=True,
        )

        self.assertEqual(head_response.status_code, 200)
        self.assertEqual(head_response.content, b"")
        self.assertEqual(post_response.status_code, 405)


class TemplateLanguageTests(SimpleTestCase):
    def test_all_project_templates_compile(self):
        root = Path(__file__).resolve().parent.parent
        for app in ("accounts", "core", "dictionary", "quiz", "errorHandler"):
            templates = root / app / "templates"
            for path in templates.rglob("*.html"):
                with self.subTest(path=path):
                    get_template(str(path.relative_to(templates)))

    def test_keyboard_changes_labels_without_changing_input_values(self):
        html = render_to_string("quiz/partials/quiz_input_panel_partial.html", {
            "keyboard_rows": [['"', '。', '小']],
        })
        self.assertIn('data-kana="&quot;"', html)
        self.assertIn('data-kana="。"', html)
        self.assertIn('゛', html)
        self.assertIn('゜', html)
        self.assertIn('1文字削除', html)

    def test_shared_choices_are_japanese_and_admin_only_labels_are_english(self):
        self.assertEqual(dict(QuizSettingForm.base_fields['vocab_type'].choices)['vocab'], '一般語彙')
        self.assertEqual(dict(VocabCreateRequestForm.base_fields['level'].choices)['0'], '未設定')
        self.assertEqual(VocabType.VOCAB.label, '一般語彙')
        self.assertEqual(VocabLevel.JLPT_N0.label, '未設定')
        self.assertEqual(dict(FeedbackCreateForm.base_fields['feedback_type'].choices)['bug_report'], '不具合の報告')
        self.assertEqual(FeedbackType.BUG_REPORT.label, '不具合の報告')
        self.assertEqual(FeedbackReplyForm.base_fields['context'].label, '返信内容')
        self.assertEqual(UserCreationAdminForm.base_fields['password2'].label, 'Confirm password')

    def test_debug_result_codes_are_preserved_and_answers_escaped(self):
        html = render_to_string('quiz/partials/quiz_result_partial.html', {
            'user': get_user_model()(is_superuser=True),
            'compared_result': [{'type': 'WRONG', 'sub_type': 'DAKUTEN', 'correct': 'が', 'answer': '<script>'}],
        })
        self.assertIn('WRONG', html)
        self.assertIn('DAKUTEN', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)

    def test_debug_result_modal_is_not_available_to_regular_users(self):
        html = render_to_string('quiz/partials/quiz_result_partial.html', {
            'user': get_user_model()(is_staff=True, is_superuser=False),
            'compared_result': [{'type': 'WRONG', 'sub_type': 'DAKUTEN', 'correct': 'が', 'answer': 'か'}],
        })
        self.assertNotIn('judgement-dialog', html)
        self.assertNotIn('DAKUTEN', html)


class InterfaceLanguageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(email='user@example.com', username='learner', password='test-password')
        cls.admin = User.objects.create_superuser(email='admin@example.com', username='reviewer', password='test-password')

    def test_public_and_admin_languages_do_not_leak_between_requests(self):
        with translation.override('fr'):
            public = self.client.get(reverse('accounts:user_login'))
            self.assertContains(public, 'メールアドレス')
            self.assertEqual(public['Content-Language'], 'ja')
            self.assertEqual(translation.get_language(), 'fr')
            admin = self.client.get(reverse('admin:login'))
            self.assertContains(admin, 'Log in')
            self.assertEqual(admin['Content-Language'], 'en-us')
            public_again = self.client.get(reverse('accounts:user_login'))
            self.assertContains(public_again, 'ログイン')
            self.assertEqual(translation.get_language(), 'fr')

    def test_builtin_validation_uses_page_language(self):
        response = self.client.post(reverse('accounts:user_login'), {})
        self.assertContains(response, 'このフィールドは必須です。')
        admin = self.client.post(reverse('admin:login'), {})
        self.assertContains(admin, 'This field is required.')

    def test_admin_uses_japanese_on_public_and_feedback_pages(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('quiz:quiz_setting'))
        self.assertEqual(response['Content-Language'], 'ja')
        feedback = self.client.get(reverse('core:feedback_list'))
        self.assertEqual(feedback['Content-Language'], 'ja')
        self.assertContains(feedback, '<html lang="ja">')
        self.assertContains(feedback, 'フィードバック一覧')
        self.assertContains(feedback, 'フィードバック')
        self.assertContains(feedback, 'ホーム')

    def test_feedback_reply_and_public_forms_are_japanese(self):
        self.client.force_login(self.admin)
        item = Feedback.objects.create(user=self.user, type='bug_report', context='Example')
        response = self.client.get(reverse('core:feedback_reply', kwargs={'feedback_pk': item.pk}))
        self.assertContains(response, '返信内容')
        self.assertContains(response, 'フィードバックに返信')
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:feedback_create'))
        self.assertContains(response, '不具合の報告')
        self.assertContains(response, '内容')

    def test_notifications_are_japanese_even_in_english_locale(self):
        with translation.override('en-us'):
            VocabRequestService.create_event_for_admin(word='猫', kana='ねこ', request_type='create', request_by=self.user)
        event = Event.objects.get(event_type='new_vocab_request')
        self.assertEqual(event.title, '単語の追加申請が送信されました。')
        self.assertEqual(event.message, 'learnerさんから「猫（ねこ）」が申請されました。')
        request = VocabRequest.objects.create(
            created_by=self.user, request_type=VocabRequestType.CREATE,
            status=VocabRequestStatus.PENDING, proposed_word='猫', proposed_kana='ねこ',
        )
        with translation.override('en-us'):
            self.assertTrue(VocabRequestService.reject_vocab_request(request, self.admin))
        self.assertIn('追加申請', Event.objects.get(event_type='vocab_request_result').title)
        self.assertIn('却下', Event.objects.get(event_type='vocab_request_result').title)

    def test_vocabulary_details_render_japanese_labels_not_internal_codes(self):
        from dictionary.models import UserVocab, Category
        vocab = Vocab.objects.create(word='猫', kana='ねこ', meaning='動物', level='1', type='vocab', is_active=True)
        category = Category.objects.create(name='daily_life', display='日常生活')
        vocab.categories.add(category)
        item = UserVocab.objects.create(user=self.user, vocab=vocab)
        self.client.force_login(self.user)
        response = self.client.get(reverse('dictionary:user_vocab_detail', kwargs={'pk': item.pk}))
        self.assertContains(response, 'N1')
        self.assertContains(response, '一般語彙')
        self.assertContains(response, '日常生活')
        self.assertNotContains(response, 'daily_life')
