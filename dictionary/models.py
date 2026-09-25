from django.db import models
from django.db.models import JSONField, Q
from django.conf import settings
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel

class VocabType(models.TextChoices):
    VOCAB = "vocab", "一般語彙"
    KATAKANA = "katakana", "カタカナ"
    # ADVERB = "adverb", "副詞"
    # MIMETIC = "mimetic", "擬音・擬態語"
    # CONJUNCTION = "conjunction", "接続詞"
    # COLLOQUIAL = "colloquial", "口語表現"

class VocabLevel(models.TextChoices):
    JLPT_N0 = "0", "未設定"
    JLPT_N1 = "1", "N1"
    JLPT_N2 = "2", "N2"
    JLPT_N3 = "3", "N3"
    JLPT_N4 = "4", "N4"
    JLPT_N5 = "5", "N5"

class Category(TimeStampedModel):
    name = models.CharField(verbose_name="Category", max_length=50, unique=True)
    display = models.CharField(verbose_name="Display name", max_length=50, blank=True, null=True)

    def __str__(self):
        return self.display or self.name
    class Meta:
        db_table = 'category'

class Vocab(TimeStampedModel):
    word = models.CharField(verbose_name="Word", max_length=50)
    word_slug = models.CharField(max_length=255, blank=True, null=True)
    meaning = models.CharField(verbose_name="Meaning", max_length=255)
    kana = models.CharField(verbose_name="Kana", max_length=255)
    is_active = models.BooleanField(verbose_name="Active", default=False)
    type = models.CharField(
        verbose_name="Type",
        max_length=20, choices=VocabType.choices
    )
    level = models.CharField(
        verbose_name="JLPT level",
        max_length=10, choices=VocabLevel.choices
    )
    categories = models.ManyToManyField(
        Category,
        related_name='vocabs',
    )

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserVocab',
        related_name='vocabs'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='created_vocab'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_vocab'
    )

    def __str__(self):
        return f"{self.word} ({self.kana})"

    class Meta:
        db_table = 'vocab'
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'kana'],
                name='word_kana_unique',
            )
        ]

class VocabDetail(models.Model):
    vocab = models.OneToOneField(
        Vocab, on_delete=models.CASCADE,
        related_name='vocab_detail'
    )
    class Meta:
        db_table = 'vocab_detail'

class KatakanaDetail(models.Model):
    native_japanese = models.CharField(max_length=255, blank=True, null=True)
    vocab = models.OneToOneField(
        Vocab, on_delete=models.CASCADE,
        related_name='katakana_detail'
    )
    class Meta:
        db_table = 'katakana_detail'

class MCSense(models.Model):
    vocab = models.ForeignKey(
        Vocab,
        on_delete=models.CASCADE,
        related_name="mc_senses"
    )
    sense_no = models.PositiveSmallIntegerField()
    sense_key = models.CharField(max_length=100, unique=True)
    meaning = models.CharField(max_length=255)
    question_1 = models.CharField(max_length=100)
    question_2 = models.CharField(max_length=100)
    mc_answer_1 = models.CharField(max_length=20)
    mc_answer_2 = models.CharField(max_length=20)
    mc_answer_3 = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.vocab.word}({self.sense_no})"

    class Meta:
        db_table = 'mc_sense'
        constraints = [
            models.UniqueConstraint(
                fields=['vocab', 'sense_no'],
                name='vocab_mc_sense_unique',
            )
        ]

class UserVocab(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_vocabs'
    )
    vocab = models.ForeignKey(
        Vocab, on_delete=models.CASCADE,
        related_name='user_vocabs'
    )
    in_use = models.BooleanField(verbose_name="Include in quizzes", default=True)
    weight = models.IntegerField(verbose_name="Selection weight", default=50, validators=[MinValueValidator(1)])
    correct_count = models.IntegerField(verbose_name="Correct answers", default=0)
    incorrect_count = models.IntegerField(verbose_name="Incorrect answers", default=0)
    streak = models.IntegerField(verbose_name="Answer streak", default=0)
    last_quiz_at = models.DateTimeField(verbose_name="Last practiced", blank=True, null=True)
    last_answer = models.CharField(verbose_name="Last answer", max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.vocab.word} ({self.vocab.kana})"

    class Meta:
        db_table = 'user_vocab'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'vocab'],
                name='user_vocab_unique',
            )
        ]
class VocabRequestType(models.TextChoices):
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"
    RESTORE = "restore", "Restore"

class VocabRequestStatus(models.TextChoices):
    NONE = "none", "None"
    PENDING = "pending", "Pending"
    REJECTED = "rejected", "Rejected"
    APPROVED = 'approved', "Approved"

class VocabRequest(TimeStampedModel):
    request_type = models.CharField(verbose_name="Request type", max_length=20, choices=VocabRequestType.choices)
    status = models.CharField(verbose_name="Status", max_length=20, choices=VocabRequestStatus.choices)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name = "applied_vocab_submissions",
        verbose_name="Created by",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name = "approved_vocab_submission",
        verbose_name="Reviewed by",
    )

    original_vocab = models.ForeignKey(
        Vocab, verbose_name="Original vocabulary entry", on_delete=models.CASCADE,
        null=True, related_name = "requests"
    )

    proposed_word = models.CharField(verbose_name="Word", max_length=50, default="word")
    proposed_vocab_type = models.CharField(verbose_name="Type", max_length=20, choices=VocabType.choices, default="vocab")
    proposed_meaning = models.CharField(verbose_name="Meaning", max_length=255, blank=True, null=True)
    proposed_kana = models.CharField(verbose_name="Kana", max_length=255, default="kana")
    proposed_level = models.CharField(verbose_name="JLPT level", max_length=10, choices=VocabLevel.choices, blank=True, null=True)
    proposed_categories = models.ManyToManyField(
        Category, verbose_name="Proposed categories",
        related_name='vocab_requests',
        blank=True,
    )

    #vocab type
    # No special fields right now.

    #katakana type
    proposed_native_japanese = models.CharField(verbose_name="Japanese equivalent", max_length=255, blank=True, null=True)

    # proposed_sense_meaning = models.CharField(max_length=255, blank=True, null=True)
    # proposed_question_1 = models.CharField(max_length=100)
    # proposed_question_2 = models.CharField(max_length=100)
    # proposed_mc_answer_1 = models.CharField(max_length=20)
    # proposed_mc_answer_2 = models.CharField(max_length=20)
    # proposed_mc_answer_3 = models.CharField(max_length=20)

    #for update type request only
    original_data = models.JSONField(verbose_name="Previous data", blank=True, null=True)


    request_reason = models.TextField(verbose_name="Request reason / source", max_length=255,blank=True,null=True)
    review_note = models.TextField(verbose_name="Review note", max_length=255,blank=True,null=True)

    def __str__(self):
        return f"{self.proposed_word}:{self.request_type}:{self.status}"

    class Meta:
        db_table = "vocab_request"
        constraints = [
            models.UniqueConstraint(
                fields=["original_vocab"],
                condition=Q(
                    status = VocabRequestStatus.PENDING,
                    original_vocab__isnull = False,
                ),
                name = "unique_pending_vocab_request_on_other",
            ),
            models.UniqueConstraint(
                fields=["proposed_word", "proposed_kana"],
                condition=Q(
                    status = VocabRequestStatus.PENDING,
                    original_vocab__isnull = True,
                ),
                name = "unique_pending_vocab_request_on_create"
            ),
        ]
