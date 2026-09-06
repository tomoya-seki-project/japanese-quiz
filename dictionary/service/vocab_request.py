from core.ui import REQUEST_TYPES_EN, REQUEST_TYPES_JA
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .vocab_action import VocabActionService

from core.service.event import EventService
from core.models import EventType

from ..models import (
    VocabType,
    VocabLevel,
    VocabRequestStatus,
    VocabRequestType,
)
from ..models import (
    Vocab,
    UserVocab,
    VocabDetail,
    KatakanaDetail,
    VocabRequest,
)

User = get_user_model()

class VocabRequestService():

    @staticmethod
    def validate_for_approval(vocab_request):
        errors = {}

        required_fields = {
            "proposed_word": "Word is required.",
            "proposed_kana": "Kana is required.",
            "proposed_vocab_type": "Vocabulary type is required.",
            "proposed_meaning": "Meaning is required.",
            "proposed_level": "Level is required.",
        }
        for field_name, error_msg in required_fields.items():
            if not getattr(vocab_request, field_name):
                errors[field_name] = error_msg
        if not vocab_request.proposed_categories.exists():
            errors["proposed_categories"] = "Select at least one category."
        match vocab_request.proposed_vocab_type:
            case VocabType.VOCAB:
                pass
            case VocabType.KATAKANA:
                if not vocab_request.proposed_native_japanese:
                    errors["proposed_native_japanese"] = (
                        "A Japanese equivalent is required for katakana words."
                    )
        if errors:
            raise ValidationError(errors)

    @staticmethod
    def build_vocab_data(vocab_request):
        return {
            "word": vocab_request.proposed_word,
            "kana": vocab_request.proposed_kana,
            "meaning": vocab_request.proposed_meaning,
            "type": vocab_request.proposed_vocab_type,
            "level": vocab_request.proposed_level,
            "categories": vocab_request.proposed_categories.all(),
            "native_japanese": vocab_request.proposed_native_japanese,
            "created_by": vocab_request.created_by,
        }

    @staticmethod
    def has_pending_request(*, target_vocab=None, word=None, kana=None):
        qs = VocabRequest.objects.filter(status = VocabRequestStatus.PENDING)

        if target_vocab is not None:
            qs = qs.filter(original_vocab = target_vocab)
        else:
            qs = qs.filter(
                proposed_word = word,
                proposed_kana = kana,
            )
        return qs.exists()

    @staticmethod
    def create_event_for_admin(*, word, kana, request_type, request_by):
        event = EventService.create_event(
                    event_type=EventType.NEW_VOCAB_REQUEST,
                    event_title=f"A new vocabulary request has been submitted: {REQUEST_TYPES_EN[request_type]}.",
                    event_msg=f"{word} ({kana}) was requested by {request_by}."
                )
        EventService.assign_event_to_users(event=event, user_list=User.objects.filter(is_staff=True))

    @staticmethod
    def gen_create_vocab_request(user, form):
        is_created = False
        word = form.cleaned_data["word"]
        kana = form.cleaned_data["kana"]
        vocab_type = form.cleaned_data["vocab_type"]
        if VocabRequestService.has_pending_request(word = word, kana = kana):
            is_created = False
        else:
            try:
                with transaction.atomic():
                    create_request = VocabRequest.objects.create(
                        created_by = user,
                        request_type = VocabRequestType.CREATE,
                        status = VocabRequestStatus.PENDING,
                        proposed_word = word,
                        proposed_vocab_type = vocab_type,
                        proposed_meaning = form.cleaned_data["meaning"],
                        proposed_kana = kana,
                        proposed_level = form.cleaned_data["level"],
                        #proposed_similar_word = form.cleaned_data["similar_word"],
                    )
                    create_request.proposed_categories.set(form.cleaned_data["categories"])
                    match vocab_type:
                        case VocabType.VOCAB:
                            pass
                        case VocabType.KATAKANA:
                            create_request.proposed_native_japanese = form.cleaned_data["native_japanese"]
                    create_request.save()
                    is_created = True

                    event_word = create_request.proposed_word
                    event_kana = create_request.proposed_kana

                    def callback():
                        VocabRequestService.create_event_for_admin(
                            word=event_word,
                            kana=event_kana,
                            request_type=VocabRequestType.CREATE,
                            request_by=user,
                        )
                    transaction.on_commit(callback)
            except IntegrityError:
                raise ValidationError("この単語には、すでに審査待ちの申請があります。")
        return is_created

    @staticmethod
    def gen_update_vocab_request(user, form):
        is_created = False
        if VocabRequestService.has_pending_request(target_vocab = form.target_vocab):
            # Add logging later.
            is_created = False
        else:
            try:
                with transaction.atomic():
                    update_request = VocabRequest.objects.create(
                        created_by = user,
                        request_type = VocabRequestType.UPDATE,
                        status = VocabRequestStatus.PENDING,
                        proposed_word = form.cleaned_data["word"],
                        proposed_vocab_type = form.cleaned_data["vocab_type"],
                        proposed_meaning = form.cleaned_data["meaning"],
                        proposed_kana = form.cleaned_data["kana"],
                        proposed_level = form.cleaned_data["level"],
                        original_vocab = form.target_vocab,
                        #proposed_similar_word = form.cleaned_data["similar_word"],
                    )
                    update_request.proposed_categories.set(form.cleaned_data["categories"])

                    update_request.original_data = {
                        "word" : form.target_vocab.word,
                        "meaning" : form.target_vocab.meaning,
                        "kana" : form.target_vocab.kana,
                        "type" : form.target_vocab.type,
                        "level" : form.target_vocab.level,
                        "categories": list(
                            form.target_vocab.categories.values_list("name", flat=True)
                        ),
                        #"similar_word": form.target_vocab.similar_word,
                    }

                    match form.cleaned_data["vocab_type"]:
                        case VocabType.VOCAB:
                            pass
                        case VocabType.KATAKANA:
                            update_request.original_data["native_japanese"] = form.target_vocab.katakana_detail.native_japanese
                            update_request.proposed_native_japanese = form.cleaned_data["native_japanese"]

                    update_request.save()
                    is_created = True

                    event_word = update_request.proposed_word
                    event_kana = update_request.proposed_kana

                    def callback():
                        VocabRequestService.create_event_for_admin(
                            word=event_word,
                            kana=event_kana,
                            request_type=VocabRequestType.UPDATE,
                            request_by=user,
                        )
                    transaction.on_commit(callback)
            except IntegrityError:
                raise ValidationError("この単語には、すでに審査待ちの申請があります。")
        return is_created

    @staticmethod
    def gen_restore_vocab_request(user, vocab):
        is_created = False
        if VocabRequestService.has_pending_request(target_vocab = vocab):
            # Add logging later.
            is_created = False
        else:
            try:
                with transaction.atomic():
                    restore_request = VocabRequest.objects.create(
                        created_by = user,
                        request_type = VocabRequestType.RESTORE,
                        status = VocabRequestStatus.PENDING,
                        proposed_word = vocab.word,
                        proposed_vocab_type = vocab.type,
                        proposed_meaning = vocab.meaning,
                        proposed_kana = vocab.kana,
                        proposed_level = vocab.level,
                        original_vocab = vocab,
                        #proposed_similar_word = vocab.similar_word,
                    )
                    restore_request.proposed_categories.set(vocab.categories.all())
                    match vocab.type:
                        case VocabType.VOCAB:
                            if hasattr(vocab, "vocab_detail"):
                                pass
                        case VocabType.KATAKANA:
                            if hasattr(vocab, "katakana_detail"):
                                restore_request.proposed_native_japanese = vocab.katakana_detail.native_japanese
                    restore_request.save()
                    is_created = True

                    event_word = restore_request.proposed_word
                    event_kana = restore_request.proposed_kana

                    def callback():
                        VocabRequestService.create_event_for_admin(
                            word=event_word,
                            kana=event_kana,
                            request_type=VocabRequestType.RESTORE,
                            request_by=user,
                        )
                    transaction.on_commit(callback)
            except IntegrityError:
                raise ValidationError("この単語には、すでに審査待ちの申請があります。")
        return is_created

    @staticmethod
    def gen_delete_vocab_request(user, vocab):
        is_created = False
        if VocabRequestService.has_pending_request(target_vocab = vocab):
            # Add logging later.
            is_created = False
        else:
            try:
                with transaction.atomic():
                    delete_request = VocabRequest.objects.create(
                        created_by = user,
                        request_type = VocabRequestType.DELETE,
                        status = VocabRequestStatus.PENDING,
                        original_vocab = vocab,
                        proposed_word = vocab.word,
                        proposed_kana = vocab.kana,
                        proposed_vocab_type = vocab.type,
                        proposed_meaning = vocab.meaning,
                        proposed_level = vocab.level,
                    )
                    delete_request.proposed_categories.set(
                        vocab.categories.all()
                    )
                    if vocab.type == VocabType.KATAKANA:
                        delete_request.proposed_native_japanese = vocab.katakana_detail.native_japanese
                        delete_request.save(update_fields=["proposed_native_japanese"])
                    is_created = True

                    event_word = delete_request.proposed_word
                    event_kana = delete_request.proposed_kana

                    def callback():
                        VocabRequestService.create_event_for_admin(
                            word=event_word,
                            kana=event_kana,
                            request_type=VocabRequestType.DELETE,
                            request_by=user,
                        )
                    transaction.on_commit(callback)
            except IntegrityError:
                raise ValidationError("この単語には、すでに審査待ちの申請があります。")
        return is_created


    @staticmethod
    def approve_vocab_request(vocab_request, reviewed_by):
        with transaction.atomic():
            locked_request = (
                VocabRequest.objects
                .select_for_update()
                .get(pk=vocab_request.pk)
            )
            if locked_request.status != VocabRequestStatus.PENDING:
                return False

            match locked_request.request_type:
                case VocabRequestType.CREATE:
                    VocabRequestService.validate_for_approval(locked_request)
                    vocab_data = VocabRequestService.build_vocab_data(vocab_request=locked_request)
                    VocabActionService.create_vocab(
                        vocab_data=vocab_data,
                        approved_by=reviewed_by
                    )
                case VocabRequestType.UPDATE:
                    if locked_request.original_vocab and locked_request.original_vocab.is_active:
                        VocabRequestService.validate_for_approval(locked_request)
                        vocab_data = VocabRequestService.build_vocab_data(vocab_request=locked_request)
                        VocabActionService.update_vocab(
                            vocab_data=vocab_data,
                            target_vocab=locked_request.original_vocab,
                            approved_by=reviewed_by
                        )
                    else:
                        raise ValidationError("The original vocabulary entry must be active for this request.")
                case VocabRequestType.RESTORE:
                    if locked_request.original_vocab and not locked_request.original_vocab.is_active:
                        VocabActionService.restore_vocab(
                            target_vocab=locked_request.original_vocab,
                            approved_by=reviewed_by
                        )
                    else:
                        raise ValidationError("The original vocabulary entry must be inactive for this request.")
                case VocabRequestType.DELETE:
                    if locked_request.original_vocab and locked_request.original_vocab.is_active:
                        VocabActionService.deactivate_vocab(
                            target_vocab=locked_request.original_vocab,
                            approved_by=reviewed_by
                        )
                    else:
                        raise ValidationError("The original vocabulary entry must be active for this request.")
            locked_request.status = VocabRequestStatus.APPROVED
            locked_request.reviewed_by = reviewed_by
            locked_request.save(
                update_fields=["status","reviewed_by","update_at"]
            )
            if locked_request.created_by is not None:
                request_result_event = EventService.create_event(
                                            event_type=EventType.VOCAB_REQUEST_RESULT,
                                            event_title=f"単語の{REQUEST_TYPES_JA[locked_request.request_type]}申請が{reviewed_by}さんに承認されました。",
                                            event_msg=""
                                        )
                EventService.assign_event_to_user(event=request_result_event, user=locked_request.created_by)
        return True

    @staticmethod
    def reject_vocab_request(vocab_request, reviewed_by):
        with transaction.atomic():
            locked_request = (
                VocabRequest.objects
                .select_for_update()
                .get(pk=vocab_request.pk)
            )
            if locked_request.status != VocabRequestStatus.PENDING:
                return False
            locked_request.status = VocabRequestStatus.REJECTED
            locked_request.reviewed_by = reviewed_by
            locked_request.save(
                update_fields=["status","reviewed_by","update_at"]
            )
            if locked_request.created_by is not None:
                request_result_event = EventService.create_event(
                                            event_type=EventType.VOCAB_REQUEST_RESULT,
                                            event_title=f"単語の{REQUEST_TYPES_JA[locked_request.request_type]}申請が{reviewed_by}さんに却下されました。",
                                            event_msg=""
                                        )
                EventService.assign_event_to_user(event=request_result_event, user=locked_request.created_by)
        return True

    @staticmethod
    def dev_clear_table():
        VocabRequest.objects.all().delete()
