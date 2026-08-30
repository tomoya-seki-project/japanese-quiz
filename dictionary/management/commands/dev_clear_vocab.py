import logging
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import authenticate

from django.db import transaction

from getpass import getpass

from ...service.vocab_action import VocabActionService
from ...service.vocab_request import VocabRequestService
from ...service.user_vocab_action import UserVocabService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clear all vocab-related data. Admin only."

    def handle(self, *args, **options):
        username = input("Admin email: ")
        password = getpass("Admin password: ")

        user = authenticate(username=username, password=password)

        if user is None:
            raise CommandError("Login failed")

        if not user.is_superuser:
            raise CommandError("Admin account is required for this command")

        last_confirm = input("Please enter CLEAR_VOCAB for final confirmation: ")

        if last_confirm != "CLEAR_VOCAB":
            self.stdout.write(self.style.WARNING("Cancelled because final confirmation failed."))
            return

        logger.info(
            "Clear vocab started: "
            "operation=%s user_id=%s",
            "dev_clear_vocab",
            user.pk,
        )

        try:
            with transaction.atomic():
                VocabRequestService.dev_clear_table()
                UserVocabService.dev_clear_table()
                VocabActionService.dev_clear_table()
        except Exception:
            logger.exception(
                "Clear vocab failed unexpectedly: "
                "operation=%s user_id=%s",
                "dev_clear_vocab",
                user.pk,
            )
            raise

        logger.info(
            "Clear vocab completed: "
            "operation=%s user_id=%s",
            "dev_clear_vocab",
            user.pk,
        )

        self.stdout.write(self.style.SUCCESS("All vocab-related tables have been cleared."))
