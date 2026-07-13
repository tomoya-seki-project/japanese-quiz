from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models import (
    Event,
    EventType,
    UserEvent,
)

from dictionary.models import (
    Vocab,
    VocabRequest,
    VocabRequestType,
    VocabRequestStatus,
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
    
    @staticmethod
    def gen_vocab_sync_event(*, user):
        last_sync = user.profile.last_vocab_sync_at
        now = timezone.now()

        if last_sync is not None:
            vocabs = Vocab.objects.filter(update_at__gt=last_sync)
        else:    
            user.profile.last_vocab_sync_at = now
            user.profile.save(update_fields=["last_vocab_sync_at", "update_at"])
            return
        
        create_count = 0
        created_word = []
        update_count = 0
        updated_word = []
        restore_count = 0
        restored_word = []
        delete_count = 0
        deleted_word = []
        
        for vocab in vocabs:
            create_vocab_request = VocabRequest.objects.filter(
                request_type = VocabRequestType.CREATE,
                proposed_word = vocab.word,
                proposed_kana = vocab.kana,
                status = VocabRequestStatus.APPROVED,
                update_at__gt = last_sync,
            ).order_by("-update_at").first()
            other_vocab_request = VocabRequest.objects.filter(
                proposed_word = vocab.word,
                proposed_kana = vocab.kana,
                status = VocabRequestStatus.APPROVED,
                update_at__gt = last_sync,
            ).exclude(
                request_type = VocabRequestType.CREATE
            ).order_by("-update_at").first()
            if create_vocab_request is None and other_vocab_request is None:
                # This vocab was created by an admin command.
                create_count += 1
                created_word.append(str(vocab))
                pass
            elif create_vocab_request is not None:
                create_count += 1
                created_word.append(str(vocab))
            if other_vocab_request is not None:   
                match(other_vocab_request.request_type):
                    case VocabRequestType.UPDATE:
                        update_count += 1
                        updated_word.append(str(vocab))
                    case VocabRequestType.RESTORE:
                        restore_count += 1
                        restored_word.append(str(vocab))
                    case VocabRequestType.DELETE:
                        delete_count += 1
                        deleted_word.append(str(vocab))

        if create_count != 0:
            create_event = EventService.create_event(
                                event_type=EventType.VOCAB,
                                event_title=f"There {"is" if create_count == 1 else "are"} {create_count} new vocab item(s) since your last vocab sync.",
                                event_msg=", ".join(created_word)
                            )
            EventService.assign_event_to_user(
                event=create_event,
                user=user,
            )        
        if update_count != 0:
            update_event = EventService.create_event(
                                event_type=EventType.VOCAB,
                                event_title=f"There {"is" if update_count == 1 else "are"} {update_count} updated vocab item(s) since your last vocab sync.",
                                event_msg=", ".join(updated_word)
                            )
            EventService.assign_event_to_user(
                event=update_event,
                user=user,
            )   
        if restore_count != 0:
            restore_event = EventService.create_event(
                                event_type=EventType.VOCAB,
                                event_title=f"There {"is" if restore_count == 1 else "are"} {restore_count} restored vocab item(s) since your last vocab sync.",
                                event_msg=", ".join(restored_word)
                            )
            EventService.assign_event_to_user(
                event=restore_event,
                user=user,
            ) 
        if delete_count != 0:
            delete_event = EventService.create_event(
                                event_type=EventType.VOCAB,
                                event_title=f"There {"is" if delete_count == 1 else "are"} {delete_count} deleted vocab item(s) since your last vocab sync.",
                                event_msg=", ".join(deleted_word)
                            )
            EventService.assign_event_to_user(
                event=delete_event,
                user=user,
            ) 
        
        user.profile.last_vocab_sync_at = now
        user.profile.save(update_fields=["last_vocab_sync_at", "update_at"])
