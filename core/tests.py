from pathlib import Path

from django.contrib.auth import get_user_model
from django.template.loader import get_template, render_to_string
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import translation

from accounts.forms import UserCreationAdminForm
from core.forms import FeedbackCreateForm, FeedbackReplyForm
from core.models import Event, Feedback, FeedbackType
from dictionary.forms import VocabCreateRequestForm
from dictionary.models import Vocab, VocabType, VocabLevel, VocabRequest, VocabRequestStatus, VocabRequestType
from dictionary.service.vocab_request import VocabRequestService
from quiz.forms import QuizSettingForm


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
        self.assertEqual(FeedbackReplyForm.base_fields['context'].label, 'Message')
        self.assertEqual(UserCreationAdminForm.base_fields['password2'].label, 'Confirm password')

    def test_debug_result_codes_are_preserved_and_answers_escaped(self):
        html = render_to_string('quiz/partials/quiz_result_partial.html', {
            'compared_result': [{'type': 'WRONG', 'sub_type': 'DAKUTEN', 'correct': 'が', 'answer': '<script>'}],
        })
        self.assertIn('WRONG', html)
        self.assertIn('DAKUTEN', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)


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

    def test_admin_uses_japanese_on_public_pages_and_english_on_feedback_pages(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('quiz:quiz_setting'))
        self.assertEqual(response['Content-Language'], 'ja')
        feedback = self.client.get(reverse('core:feedback_list'))
        self.assertEqual(feedback['Content-Language'], 'en-us')
        self.assertContains(feedback, '<html lang="en-us">')
        self.assertContains(feedback, 'Feedback')
        self.assertContains(feedback, 'フィードバック')
        self.assertContains(feedback, 'ホーム')

    def test_feedback_reply_form_is_english_and_public_form_is_japanese(self):
        self.client.force_login(self.admin)
        item = Feedback.objects.create(user=self.user, type='bug_report', context='Example')
        response = self.client.get(reverse('core:feedback_reply', kwargs={'feedback_pk': item.pk}))
        self.assertContains(response, 'Message')
        self.assertContains(response, 'Reply to feedback')
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:feedback_create'))
        self.assertContains(response, '不具合の報告')
        self.assertContains(response, '内容')

    def test_notification_language_follows_recipient_not_current_locale(self):
        with translation.override('ja'):
            VocabRequestService.create_event_for_admin(word='猫', kana='ねこ', request_type='create', request_by=self.user)
        self.assertIn('Creation', Event.objects.get(event_type='new_vocab_request').title)
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
