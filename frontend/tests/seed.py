"""Generate deterministic local browser fixtures in the isolated test database."""
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "frontend.tests.settings"
import django
django.setup()
from django.conf import settings
from django.core.management import call_command
from accounts.models import User
from dictionary.models import Category, Vocab, UserVocab, KatakanaDetail, MCSense
from core.models import Event, UserEvent, Feedback

call_command("migrate", verbosity=0)
user, created = User.objects.get_or_create(email="ui@example.test", defaults={"username":"テストユーザー", "is_active":True, "is_staff":True, "is_superuser":True})
if created:
    user.set_password("ui-preview-password")
    user.save()
categories = [Category.objects.get_or_create(name=f"UI {i}", defaults={"display":name})[0] for i,name in enumerate(["日常生活", "学校・勉強", "仕事", "食べ物", "旅行", "気持ち"])]
for i in range(65):
    vocab, _ = Vocab.objects.get_or_create(word=f"練習{i:02}", kana="れんしゅう", defaults={"meaning":"毎日少しずつ日本語を覚えること。", "type":"vocab", "level":"5", "is_active":True})
    vocab.categories.set(categories[:3])
    UserVocab.objects.get_or_create(user=user, vocab=vocab)
vocab, _ = Vocab.objects.get_or_create(word="Google Calendar integration with a very long example", kana="ググる", defaults={"meaning":"インターネットで検索すること", "type":"katakana", "level":"0", "is_active":True})
KatakanaDetail.objects.get_or_create(vocab=vocab, defaults={"native_japanese":"検索する"})
vocab.categories.set(categories[:3])
MCSense.objects.get_or_create(vocab=vocab, sense_no=1, defaults={"sense_key":"ui-example-1", "meaning":"検索すること", "question_1":"わからなければ____(て)ください。", "question_2":"まず____ことが大切です。", "mc_answer_1":"A", "mc_answer_2":"B", "mc_answer_3":"C"})
UserVocab.objects.get_or_create(user=user, vocab=vocab, defaults={"weight":275,"streak":-3,"last_answer":"ググった"})
for i in range(12):
    event, _ = Event.objects.get_or_create(title=f"お知らせ {i}：単語帳に新しい内容が届きました。詳細を確認してください。", defaults={"event_type":"feedback_reply", "message":"ご利用ありがとうございます。\nこれはUI確認用の通知です。"})
    UserEvent.objects.get_or_create(user=user, event=event)
    Feedback.objects.get_or_create(user=user, context=f"UI確認用のフィードバック {i}\n改行を含む内容です。", defaults={"type":"feature_request","status":["pending","replied","closed"][i % 3]})
print("Isolated UI fixtures ready:", settings.DATABASES["default"]["NAME"])
