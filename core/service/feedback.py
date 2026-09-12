from django.utils import timezone

from django.db import transaction

from django.core.exceptions import ValidationError

from ..models import (
    Event,
    EventType,
    UserEvent,
    Feedback,
    FeedbackStatus,
    FeedbackType,
)

from .event import EventService

class FeedbackService():

    @staticmethod
    def create_feedback(*, user, feedback_type, context):
        is_doubled = Feedback.objects.filter(
            user=user,
            type=feedback_type,
            context=context,
            status=FeedbackStatus.PENDING
        ).exists()

        if is_doubled:
            return None, is_doubled

        user_feedback = Feedback.objects.create(
            user=user,
            type=feedback_type,
            status=FeedbackStatus.PENDING,
            context=context,
        )
        return user_feedback, is_doubled

    @staticmethod
    def reply_feedback(*, admin_user, target_feedback, reply_context, is_close):

        with transaction.atomic():
            target_feedback = Feedback.objects.select_for_update().get(pk=target_feedback.pk)
            if target_feedback.status == FeedbackStatus.CLOSED:
                raise ValidationError(
                    "this feedback case already closed!"
            )


            reply_event = EventService.create_event(
                event_type=EventType.FEEDBACK_REPLY,
                event_title="フィードバックをお寄せいただき、ありがとうございます。",
                event_msg=reply_context
            )
            EventService.assign_event_to_user(
                user=target_feedback.user,
                event=reply_event,
            )
            if is_close:
                target_feedback.status = FeedbackStatus.CLOSED
            else:
                target_feedback.status = FeedbackStatus.REPLIED
            target_feedback.reply_by = admin_user
            target_feedback.reply_at = timezone.now()
            target_feedback.update_at = timezone.now()
            target_feedback.save(update_fields=["status", "reply_by", "reply_at", "update_at"])
        return reply_event