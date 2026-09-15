from django.db import models
import uuid
from config import settings

from dictionary.models import UserVocab
from core.models import TimeStampedModel


class QuizAttempt(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ANSWERED = "answered", "Answered"
        SKIPPED = "skipped", "Skipped"

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    user_vocab = models.ForeignKey(
        UserVocab,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    processed_at = models.DateTimeField(
        null=True,blank=True
    )

    class Meta:
        db_table = "quiz_attempt"
