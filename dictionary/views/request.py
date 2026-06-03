from ..models import (
    Vocab,
    UserVocab,
    VocabType,
    VocabCategory,
    VocabLevel,
    KanjiDetail,
    KatakanaDetail,
    VocabRequest,
    VocabRequestStatus,
    VocabRequestType,
)

def genCreateVocabRequest(user, form):
    is_created = False
    word = form.cleaned_data["word"]
    kana = form.cleaned_data["kana"]
    vocab_type = form.cleaned_data["vocab_type"]
    request = VocabRequest.objects.filter(
        request_type = VocabRequestType.CREATE,
        status = VocabRequestStatus.PENDING,
        proposed_word = word,
        proposed_kana = kana,
    ).first()
    if request:
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
            proposed_category = form.cleaned_data["category"]
        )
        match vocab_type:
            case VocabType.KANJI:
                create_request.proposed_similar_kanji = form.cleaned_data["similar_kanji"]
            case VocabType.KATAKANA:
                create_request.proposed_original_word = form.cleaned_data["original_word"]
                create_request.proposed_native_japanese = form.cleaned_data["native_japanese"]
        create_request.save()
        is_created = True
    return is_created

def genUpdateVocabRequest(user, form):
    pass

def genRestoreVocabRequest(user, vocab):
    is_created = False
    request = VocabRequest.objects.filter(
        request_type = VocabRequestType.RESTORE,
        status = VocabRequestStatus.PENDING,
        proposed_word = vocab.word,
        proposed_kana = vocab.kana,
    ).first()
    if request:
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
        )
        match vocab.type:
            case VocabType.KANJI:
                if hasattr(vocab, "kanji_detail"):
                    restore_request.proposed_similar_kanji = vocab.kanji_detail.similar_kanji
            case VocabType.KATAKANA:
                if hasattr(vocab, "katakana_detail"):
                    restore_request.proposed_original_word = vocab.katakana_detail.original_word
                    restore_request.proposed_native_japanese = vocab.katakana_detail.native_japanese
        restore_request.save()
        is_created = True
    return is_created

def genDeleteVocabRequest(user, vocab):
    pass