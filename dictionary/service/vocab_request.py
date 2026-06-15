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
        # request = VocabRequest.objects.filter(
        #     #request_type = VocabRequestType.CREATE,
        #     status = VocabRequestStatus.PENDING,
        #     proposed_word = word,
        #     proposed_kana = kana,
        # ).exists()
        # if request:
        #     pass
        if VocabRequestService.hasPendingRequest(word = word, kana = kana):
            is_created = False
        else:
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
                proposed_similar_word = form.cleaned_data["similar_word"],
            )
            match vocab_type:
                case VocabType.VOCAB:
                    pass
                case VocabType.KATAKANA:
                    create_request.proposed_native_japanese = form.cleaned_data["native_japanese"]
            create_request.save()
            is_created = True
        return is_created
    
    @staticmethod
    def genUpdateVocabRequest(user, form):
        is_created = False
        # request = VocabRequest.objects.filter(
        #     status = VocabRequestStatus.PENDING,
        #     proposed_word = form.target_vocab.word,
        #     proposed_kana = form.target_vocab.kana
        # ).exists()
        # if request:
        #     pass
        if VocabRequestService.hasPendingRequest(target_vocab = form.target_vocab):
            #add log
            is_created = False
        else:
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
                proposed_similar_word = form.cleaned_data["similar_word"],
            )
            
            update_request.original_data = {
                "word" : form.target_vocab.word,
                "meaning" : form.target_vocab.meaning,
                "kana" : form.target_vocab.kana,
                "type" : form.target_vocab.type,
                "level" : form.target_vocab.level,
                "category": form.target_vocab.category,
                "similar_word": form.target_vocab.similar_word,
            }
            
            match form.cleaned_data["vocab_type"]:
                case VocabType.VOCAB:
                    pass
                case VocabType.KATAKANA:
                    update_request.original_data["native_japanese"] = form.target_vocab.katakana_detail.native_japanese
                    update_request.proposed_native_japanese = form.cleaned_data["native_japanese"]

            
            update_request.save()
            is_created = True
        return is_created

    @staticmethod
    def genRestoreVocabRequest(user, vocab):
        is_created = False
        # request = VocabRequest.objects.filter(
        #     #request_type = VocabRequestType.RESTORE,
        #     status = VocabRequestStatus.PENDING,
        #     proposed_word = vocab.word,
        #     proposed_kana = vocab.kana,
        # ).exists()
        # if request:
        #     pass
        if VocabRequestService.hasPendingRequest(target_vocab = vocab):
            # add log
            is_created = False
        else:
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
                proposed_similar_word = vocab.similar_word,
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
        return is_created

    @staticmethod
    def genDeleteVocabRequest(user, vocab):
        is_created = False
        # request = VocabRequest.objects.filter(
        #     status = VocabRequestStatus.PENDING,
        #     original_vocab = vocab,
        # ).exists()
        # if request:
        if VocabRequestService.hasPendingRequest(target_vocab = vocab):
            #add log
            is_created = False
        else:
            delete_request = VocabRequest.objects.create(
                created_by = user,
                request_type = VocabRequestType.DELETE,
                status = VocabRequestStatus.PENDING,
                original_vocab = vocab,
            )
            is_created = True
        return is_created


    @staticmethod
    def approveVocabRequest(vocab_request, reviewed_by):
        print('approveVocabRequest')

    @staticmethod
    def rejectVocabRequest(vocab_request, reviewed_by):
        print('rejectVocabRequest')
