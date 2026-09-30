import logging
from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError

from django.db import transaction

from ...service.user_vocab_action import UserVocabService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "adjust user vocab's weight if last quiz time more than setting days"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how manay user vocabs weight would be adjusted without adjusting them.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        adjusted_count = 0

        if dry_run:
            return

        logger.info(
            "Clear vocab completed: "
            "operation=%s adjusted_count=%s",
            "adjust_user_vocab_weight",
            adjusted_count,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{adjusted_count} user vocab's weight have been adjusted."
            )
        )
