from django.db import models
from django.conf import settings
from datetime import date, datetime

class EventType(models.TextChoices):
    VOCAB_REQUEST_RESULT = "vocab_request_result", "Vocab Request Result"
    NEW_VOCAB_REQUEST = "new_vocab_request", "New Vocab Request Result"
    VOCAB = "vocab", "Vocab"
    WEIGHT_UPDATE_BY_SYSTEM = "weight_update_by_system", "Weight Update by System"
    FEEDBACK_REPLY = "feedback_reply", "Feedback Reply"

class FeedbackType(models.TextChoices):
    VOCAB_SUGGESTION = "vocab_suggestion", "Vocab Suggestion"
    BULK_VOCAB_REQUEST = "bulk_vocab_request", "Bulk Vocab Request"
    BUG_REPORT = "bug_report", "Bug Report"
    FEATURE_REQUEST = "feature_request", "Feature Request"
    OTHERS = "others", "Others"

class FeedbackStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    REPLIED = "replied", "Replied"

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

class Feedback(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    type = models.CharField(
        max_length=50,
        choices=FeedbackType.choices
    )
    status = models.CharField(
        max_length=50,
        blank=True,null=True,
        choices=FeedbackStatus.choices
    )
    context = models.TextField()

    reply_at = models.DateTimeField(blank=True, null=True)
    reply_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='Replied_feedbacks'
    )

    class Meta:
        db_table = 'feedback'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['user', 'type', 'context'],
        #         name='Feedback_unique',
        #     )
        # ]