from django.db import models
from django.db.models import JSONField
from django.conf import settings
from core.models import TimeStampedModel



class VocabType(models.TextChoices):
    VOCAB = "vocab", "Vocab"
    KATAKANA = "katakana", "Katakana"

class VocabLevel(models.TextChoices):
    JLPT_N1 = "N1", "N1"
    JLPT_N2 = "N2", "N2"
    JLPT_N3 = "N3", "N3"
    JLPT_N4 = "N4", "N4"
    JLPT_N5 = "N5", "N5"

class VocabCategory(models.TextChoices):
    LIFE = "life", "Life"

class Vocab(TimeStampedModel):
    word = models.CharField(max_length=50)
    word_slug = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255)
    kana = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    type = models.CharField(
        max_length=20, choices=VocabType.choices
        )
    level = models.CharField(
        max_length=10, choices=VocabLevel.choices
        )
    category = models.CharField(
        max_length=20, choices=VocabCategory.choices
        )
    
    similar_word = models.CharField(max_length=255, blank=True, null=True)

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

    class Meta:
        db_table = 'vocab'
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'kana'],
                name='word_kana_unique',
            )
        ]

class VocabDetail(TimeStampedModel):
    vocab = models.OneToOneField(
        Vocab, on_delete=models.CASCADE,
        related_name='vocab_detail'
        )
    class Meta:
        db_table = 'vocab_detail'

class KatakanaDetail(TimeStampedModel):
    original_word = models.CharField(max_length=255, blank=True, null=True)
    native_japanese = models.CharField(max_length=255, blank=True, null=True)
    vocab = models.OneToOneField(
        Vocab, on_delete=models.CASCADE,
        related_name='katakana_detail'
    )
    class Meta:
        db_table = 'katakana_detail'

class UserVocab(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='user_vocab'
    )
    vocab = models.ForeignKey(
        Vocab, on_delete=models.CASCADE,
        related_name='user_vocab'
    )
    weight = models.IntegerField(default=50)
    correct_count = models.IntegerField(default=0)
    incorrect_count = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_quiz_at = models.DateTimeField(blank=True, null=True)
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
    REVIEW = "review", "Review"
    RESTORE = "restore", "Restore"

class VocabRequestStatus(models.TextChoices):
    NONE = "none", "None"
    PENDING = "pending", "Pending"
    REJECTED = "rejected", "Rejected"
    APPROVED = 'approved', "Approved"

class VocabRequest(TimeStampedModel):
    request_type = models.CharField(max_length=20, choices=VocabRequestType.choices)
    status = models.CharField(max_length=20, choices=VocabRequestStatus.choices)
    reason = models.CharField(max_length=255,blank=True,null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name = "applied_vocab_submissions"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name = "approved_vocab_submission"
    )

    original_vocab = models.ForeignKey(
        Vocab, on_delete=models.CASCADE,
        null=True, related_name = "submissions"
    )

    proposed_word = models.CharField(max_length=50, blank=True, null=True)
    proposed_vocab_type = models.CharField(max_length=20, choices=VocabType.choices, blank=True, null=True)
    proposed_meaning = models.CharField(max_length=255, blank=True, null=True)
    proposed_kana = models.CharField(max_length=255, blank=True, null=True)
    proposed_level = models.CharField(max_length=10, choices=VocabLevel.choices, blank=True, null=True)
    proposed_category = models.CharField(max_length=20, choices=VocabCategory.choices, blank=True, null=True)

    proposed_similar_word = models.CharField(max_length=255, blank=True, null=True)
    
    #vocab type
    # nothing special right now

    #katakana type
    proposed_original_word = models.CharField(max_length=255, blank=True, null=True)
    proposed_native_japanese = models.CharField(max_length=255, blank=True, null=True)

    #for update type request only
    original_data = models.JSONField(blank=True, null=True)
    class Meta:
        db_table = "vocab_request"
