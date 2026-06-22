from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.urls import path, reverse

from ..models import (
    Vocab,
    UserVocab,
)

class UserVocabService():
    
    @staticmethod
    def get_new_vocab(*, user, limit=50):
        vocab_ids = (
            Vocab.objects
            .exclude(user_vocab__user=user)
            .order_by("-id")
            .values_list("id", flat=True)[:limit]
        )
        return Vocab.objects.filter(id__in=vocab_ids)
    
    @staticmethod
    def create_user_vocabs(*, user, vocabs):
        for vocab in vocabs:
            with transaction.atomic():
                user_vocab, created = UserVocab.objects.get_or_create(
                    user=user,
                    vocab=vocab
                )

