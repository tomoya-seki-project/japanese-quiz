from django.db import models
from django.conf import settings
from datetime import date, datetime

class EventType(models.TextChoices):
    VOCAB_REQUEST_RESULT = "vocab_request_result","Vocab Request Result"
    NEW_VOCAB_REQUEST = "new_vocab_request","New Vocab Request Result"
    VOCAB = "vocab","Vocab"
    WEIGHT_UPDATE_BY_SYSTEM = "weight_update_by_system","Weight Update by System"


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