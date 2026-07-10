from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import (
    Event,
    EventType,
    UserEvent,
)

User = get_user_model()

class EventService():

    @staticmethod
    def gen_event_message():
        pass

    @staticmethod
    def create_event(*, event_type, event_title, event_msg):
        event = Event.objects.create(
            event_type=event_type,
            title=event_title,
            message=event_msg,
        )
        return event

    @staticmethod
    def assign_event_to_user(*, event, user):
        UserEvent.objects.get_or_create(event=event, user=user)

    @staticmethod
    def assign_event_to_users(*, event, user_list=None):
        if user_list is None:
            user_list = User.objects.all()
        for user in user_list:
            EventService.assign_event_to_user(event=event, user=user)

    @staticmethod
    def mark_as_read(*,user, user_event_id):
        user_event = UserEvent.objects.get(user=user, pk=user_event_id)
        user_event.is_read = True
        user_event.read_at = timezone.now()
        user_event.save()

    @staticmethod
    def get_unread_events(*, user):
        return UserEvent.objects.filter(user=user, is_read=False).order_by("-event__create_at").select_related("event")