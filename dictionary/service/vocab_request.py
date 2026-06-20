from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

from .vocab_action import VocabActionService

from ..models import (
    VocabType,
    VocabCategory,
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

class VocabRequestService():

    @staticmethod
    def validate_for_approval(vocab_request):
        errors = {}

        required_fields = {
            "proposed_word": "Word is required.",
            "proposed_kana": "Kana is required.",
            "proposed_vocab_type": "Vocab type is required.",
            "proposed_meaning": "Meaning is required.",
            "proposed_level": "Level is required.",
            "proposed_category": "Category is required.",
        }
        for field_name, error_msg in required_fields.items():
            if not getattr(vocab_request, field_name):
                errors[field_name] = error_msg
        match vocab_request.proposed_vocab_type:
            case VocabType.VOCAB:
                pass
            case VocabType.KATAKANA:
                if not vocab_request.proposed_native_japanese:
                    errors["proposed_native_japanese"] = (
                        "Native Japanese is required for Katakana"
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
            "category": vocab_request.proposed_category,
            "native_japanese": vocab_request.proposed_native_japanese,
            "created_by": vocab_request.created_by,
        }
    
    @staticmethod
    def hasPendingRequest(*, target_vocab=None, word=None, kana=None):
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
    def genCreateVocabRequest(user, form):
        is_created = False
        word = form.cleaned_data["word"]
        kana = form.cleaned_data["kana"]
        vocab_type = form.cleaned_data["vocab_type"]
        if VocabRequestService.hasPendingRequest(word = word, kana = kana):
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
                        proposed_category = form.cleaned_data["category"],
                        #proposed_similar_word = form.cleaned_data["similar_word"],
                    )
                    match vocab_type:
                        case VocabType.VOCAB:
                            pass
                        case VocabType.KATAKANA:
                            create_request.proposed_native_japanese = form.cleaned_data["native_japanese"]
                    create_request.save()
                    is_created = True
            except IntegrityError:
                raise ValidationError("This word have another request waiting for review already")
        return is_created
    
    @staticmethod
    def genUpdateVocabRequest(user, form):
        is_created = False
        if VocabRequestService.hasPendingRequest(target_vocab = form.target_vocab):
            #add log
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
                        proposed_category = form.cleaned_data["category"],
                        original_vocab = form.target_vocab,
                        #proposed_similar_word = form.cleaned_data["similar_word"],
                    )
                    
                    update_request.original_data = {
                        "word" : form.target_vocab.word,
                        "meaning" : form.target_vocab.meaning,
                        "kana" : form.target_vocab.kana,
                        "type" : form.target_vocab.type,
                        "level" : form.target_vocab.level,
                        "category": form.target_vocab.category,
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
            except IntegrityError:
                raise ValidationError("This word have another request waiting for review already")
        return is_created

    @staticmethod
    def genRestoreVocabRequest(user, vocab):
        is_created = False
        if VocabRequestService.hasPendingRequest(target_vocab = vocab):
            # add log
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
                        proposed_category = vocab.category,
                        original_vocab = vocab,
                        #proposed_similar_word = vocab.similar_word,
                    )
                    match vocab.type:
                        case VocabType.VOCAB:
                            if hasattr(vocab, "vocab_detail"):
                                pass
                        case VocabType.KATAKANA:
                            if hasattr(vocab, "katakana_detail"):
                                restore_request.proposed_native_japanese = vocab.katakana_detail.native_japanese
                    restore_request.save()
                    is_created = True
            except IntegrityError:
                raise ValidationError("This word have another request waiting for review already")
        return is_created

    @staticmethod
    def genDeleteVocabRequest(user, vocab):
        is_created = False
        if VocabRequestService.hasPendingRequest(target_vocab = vocab):
            #add log
            is_created = False
        else:
            try:
                with transaction.atomic():
                    delete_request = VocabRequest.objects.create(
                        created_by = user,
                        request_type = VocabRequestType.DELETE,
                        status = VocabRequestStatus.PENDING,
                        original_vocab = vocab,
                    )
                    is_created = True
            except IntegrityError:
                raise ValidationError("This word have another request waiting for review already")
        return is_created


    @staticmethod
    def approveVocabRequest(vocab_request, reviewed_by):
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
                    VocabActionService.createVocab(
                        vocab_data=vocab_data, 
                        approved_by=reviewed_by
                    )
                case VocabRequestType.UPDATE:
                    VocabRequestService.validate_for_approval(locked_request)
                    vocab_data = VocabRequestService.build_vocab_data(vocab_request=locked_request)
                    VocabActionService.updateVocab(
                        vocab_data=vocab_data, 
                        target_vocab=locked_request.original_vocab, 
                        approved_by=reviewed_by
                    )
                case VocabRequestType.RESTORE:
                    VocabActionService.restoreVocab(
                        target_vocab=locked_request.original_vocab, 
                        approved_by=reviewed_by
                    )
                case VocabRequestType.DELETE:
                    VocabActionService.deactivateVocab(
                        target_vocab=locked_request.original_vocab,
                        approved_by=reviewed_by
                    )
            locked_request.status = VocabRequestStatus.APPROVED
            locked_request.reviewed_by = reviewed_by
            locked_request.save(
                update_fields=["status","reviewed_by","update_at"]
            )
        return True

    @staticmethod
    def rejectVocabRequest(vocab_request, reviewed_by):
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
        return True
