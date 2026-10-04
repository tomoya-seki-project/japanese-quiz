from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.urls import path, reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

import logging

from ..models import (
    Vocab,
    UserVocab,
)

from core.service.event import EventService

logger = logging.getLogger(__name__)
User = get_user_model()

class UserVocabService():

    @staticmethod
    def get_new_vocab(*, user, limit=50):
        vocab_ids = (
            Vocab.objects
            .filter(is_active=True)
            .exclude(user_vocabs__user=user)
            .order_by("-id")
            .values_list("id", flat=True)#[:limit]
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

    @staticmethod
    def sync_new_vocab(*, user):
        with transaction.atomic():
            User.objects.select_for_update().get(pk=user.pk)
            existing_vocab_ids = UserVocab.objects.filter(
                user=user,
            ).values_list("vocab_id", flat=True)

            new_vocab_ids = Vocab.objects.filter(
                is_active=True,
            ).exclude(
                id__in=existing_vocab_ids,
            ).values_list("id", flat=True)

            user_vocabs = [
                UserVocab(user=user, vocab_id=vocab_id)
                for vocab_id in new_vocab_ids
            ]
            before_sync_count = UserVocab.objects.filter(user=user).count()
            UserVocab.objects.bulk_create(
                user_vocabs,
                ignore_conflicts=True,
            )
            after_sync_count = UserVocab.objects.filter(user=user).count()
            return max(after_sync_count - before_sync_count, 0)
        return 0

    @staticmethod
    def dev_clear_table():
        UserVocab.objects.all().delete()

    @staticmethod
    def sync_vocab_safely(*, user):
        try:
            created_count = UserVocabService.sync_new_vocab(user=user)
        except Exception as e:
            logger.exception(
                "User vocab sync failed: "
                "operation=%s user_id=%s",
                "user_vocab_sync",
                user.pk,
            )
            return

        if created_count > 0:
            logger.info(
                "User vocab sync completed: "
                "operation=%s user_id=%s created_count=%s",
                "user_vocab_sync",
                user.pk,
                created_count,
            )
        try:
            EventService.gen_vocab_sync_event(user=user)
        except Exception as e:
            logger.exception(
                "User vocab sync event generation failed: "
                "operation=%s user_id=%s",
                "user_vocab_sync_event_generation",
                user.pk,
            )

    @staticmethod
    @transaction.atomic
    def set_user_vocabs_in_use_status(*, user, selected_ids, selectable_ids):
        selectable_qs = UserVocab.objects.filter(
            user=user,
            id__in=selectable_ids,
        )

        get_unselect_qs = selectable_qs.filter(
            in_use=True,
        ).exclude(
            id__in=selected_ids,
        )
        get_select_qs = selectable_qs.filter(
            in_use=False,
            id__in=selected_ids,
        )
        now = timezone.now()
        deactivated_count = get_unselect_qs.update(in_use=False, update_at=now)
        activated_count = get_select_qs.update(in_use=True, update_at=now)
        return activated_count, deactivated_count