from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimeStampedModel

User = get_user_model()

class Vocab(TimeStampedModel):
    TYPE_CHOICES = [
        ('kanji', 'kanji'),
        ('katakana', 'katakana'),
    ]
    LEVEL_CHOICES = [
        ('N1','N1'),
        ('N2','N2'),
        ('N3','N3'),
        ('N4','N4'),
        ('N5','N5'),
    ]
    CATEGORY_CHOICES = [
        ('normal','normal')
    ]
    STATUS_CHOICES = [
        ('none', 'None'),
        ('pending', 'pending'),
        ('on_hold', 'on hold'),
        ('rejected', 'rejected'),
    ]

    word = models.CharField(max_length=50)
    word_slug = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES
        )
    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES
        )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES
        )
    status = models.CharField(
        max_length=40, choices=STATUS_CHOICES, default='none'
    )

    users = models.ManyToManyField(
        User,
        through='UserVocab',
        related_name='vocab'
    )
    
    created_by = models.ForeignKey(
        User, null=True, blank=True, 
        on_delete=models.SET_NULL,
        related_name='created_vocab'
        )
    approved_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_vocab'
    )

    class Meta:
        db_table = 'vocab'
        constraints = [
            models.UniqueConstraint(
                fields=['word', 'answer'],
                name='word_and_answer'
            )
        ]


class KanjiDetail(TimeStampedModel):
    vocab = models.OneToOneField(
        Vocab, on_delete=models.CASCADE,
        related_name='kanji_detail'
        )
    class Meta:
        db_table = 'kanji_detail'

class KatakanaDetail(TimeStampedModel):
    vocab = models.OneToOneField(
        Vocab, on_delete=models.CASCADE,
        related_name='katakana_detail'
    )
    class Meta:
        db_table = 'katakana_detail'

class UserVocab(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_vocab')
    vocab = models.ForeignKey(
        Vocab, on_delete=models.CASCADE,
        related_name='user_vocab'
    )
    weight = models.IntegerField(default=50)
    correct_times = models.IntegerField()
    incorrect_times = models.IntegerField()
    last_quiz_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_vocab'