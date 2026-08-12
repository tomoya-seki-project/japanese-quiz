from django.db import models
from django.conf import settings
from datetime import date, datetime

class EventType(models.TextChoices):
    VOCAB_REQUEST_RESULT = "vocab_request_result", "Vocab Request Result"
    NEW_VOCAB_REQUEST = "new_vocab_request", "New Vocab Request Result"
    VOCAB = "vocab", "Vocab"
    WEIGHT_UPDATE_BY_SYSTEM = "weight_update_by_system", "Weight Update by System"
    FAQ_REPLY = "FAQ_reply", "FAQ Reply"

class FAQType(models.TextChoices):
    DICTIONARY_RELATED = "dictionary_related", "Dictionary Related"
    QUIZ_RELATED = "quiz_related", "Quiz Related"
    ACCOUNT_RELATED = "account_related", "Account Related"
    OTHERS = "others", "Others"

class TimeStampedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Event(models.Model):
    event_type = models.CharField(
        verbose_name="Event",
        max_length=100,
        choices=EventType.choices
    )
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserEvent',
        related_name='events'
    )

    def __str__(self):
        return f"{self.event_type} : {self.title}"

    class Meta:
        db_table = 'event'

class UserEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_events'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='user_events'
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_event'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='user_event_unique',
            )
        ]

class FAQ(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='FAQs'
    )
    type = models.CharField(
        max_length=50,
        choices=FAQType.choices
    )
    context = models.TextField()

    reply_at = models.DateTimeField(blank=True, null=True)
    reply_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='Replied_FAQs'
    )

    class Meta:
        db_table = 'FAQ'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'type', 'context'],
                name='FAQ_unique',
            )
        ]