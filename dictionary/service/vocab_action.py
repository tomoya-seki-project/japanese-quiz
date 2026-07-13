from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

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
    Category,
)

class VocabActionService():

    @staticmethod
    def create_vocab(vocab_data, approved_by):
        with transaction.atomic():
            vocab = Vocab(
                word=vocab_data["word"],
                kana=vocab_data["kana"],
                meaning=vocab_data["meaning"],
                type=vocab_data["type"],
                level=vocab_data["level"],
                is_active=True,
                created_by=vocab_data["created_by"],
                approved_by=approved_by,
            )
            vocab.full_clean()
            vocab.save()
            vocab.categories.set(vocab_data["categories"])
            match vocab_data["type"]:
                case VocabType.VOCAB:
                    VocabDetail.objects.create(
                        vocab=vocab,
                    )
                case VocabType.KATAKANA:
                    KatakanaDetail.objects.create(
                        vocab=vocab,
                        native_japanese=vocab_data["native_japanese"],
                    )
        return vocab if vocab else None

    @staticmethod
    def update_vocab(vocab_data, target_vocab, approved_by):
        update_success = False
        with transaction.atomic():
            target_vocab.word=vocab_data["word"]
            target_vocab.kana=vocab_data["kana"]
            target_vocab.meaning=vocab_data["meaning"]
            target_vocab.level=vocab_data["level"]
            target_vocab.approved_by=approved_by
            # Decide later whether updates should also change created_by.
            # target_vocab.created_by=vocab_data["created_by"]
            target_vocab.full_clean()
            target_vocab.save()
            target_vocab.categories.set(vocab_data["categories"])
            match vocab_data["type"]:
                case VocabType.VOCAB:
                    pass
                case VocabType.KATAKANA:
                    if hasattr(target_vocab, "katakana_detail"):
                        target_vocab.katakana_detail.native_japanese=vocab_data["native_japanese"]
                        target_vocab.katakana_detail.save()
            update_success = True

        return target_vocab if update_success else None
        

    @staticmethod
    def deactivate_vocab(target_vocab, approved_by):
        target_vocab.is_active = False
        target_vocab.approved_by = approved_by
        target_vocab.save(update_fields=['is_active', 'approved_by', 'update_at'])
    
    @staticmethod
    def restore_vocab(target_vocab, approved_by):
        target_vocab.is_active = True
        target_vocab.approved_by = approved_by
        target_vocab.save(update_fields=['is_active', 'approved_by', 'update_at'])

    @staticmethod
    def dev_clear_table():
        VocabDetail.objects.all().delete()
        KatakanaDetail.objects.all().delete()
        Vocab.objects.all().delete()
        Category.objects.all().delete()
