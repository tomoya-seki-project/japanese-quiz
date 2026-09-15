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

from ..validators import validate_category_count

class VocabActionService():

    @staticmethod
    def create_vocab(vocab_data, approved_by):
        if vocab_data["type"] != VocabType.VOCAB and vocab_data["type"] != VocabType.KATAKANA:
            return None
        categories_list = validate_category_count(vocab_data["categories"], min_count=1)
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
            vocab.categories.set(categories_list)
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
        if vocab_data["type"] != VocabType.VOCAB and vocab_data["type"] != VocabType.KATAKANA:
            return None
        categories_list = validate_category_count(vocab_data["categories"], min_count=1)
        update_success = False
        with transaction.atomic():
            target_vocab.word=vocab_data["word"]
            target_vocab.kana=vocab_data["kana"]
            target_vocab.meaning=vocab_data["meaning"]
            target_vocab.level=vocab_data["level"]
            target_vocab.approved_by=approved_by
            target_vocab.full_clean()
            target_vocab.save()
            target_vocab.categories.set(categories_list)
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
