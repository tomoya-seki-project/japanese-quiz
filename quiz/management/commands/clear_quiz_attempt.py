import logging
from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError

from quiz.models import QuizAttempt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Clear old quiz attempt(more than 7 days)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Delete completed attempts older than this number of days.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many attempts would be deleted without deleting them."
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]
        if days < 1:
            raise CommandError("--days must be at least 1.")


        logger.info(
            "Clear quiz attempts started: "
            "operation=%s",
            "clear_quiz_attempt",
        )


        cutoff_time = timezone.now() - timedelta(days=days)
        old_quiz_attempt_qs = QuizAttempt.objects.filter(processed_at__lte=cutoff_time).exclude(status=QuizAttempt.Status.PENDING)

        if dry_run:
            candidate_count = old_quiz_attempt_qs.count()
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run: {candidate_count} quiz attempt(s) would be deleted."
                )
            )
            return

        deleted_count, detail = old_quiz_attempt_qs.delete()

        logger.info(
            "Clear quiz attempts completed: "
            "operation=%s deleted_count=%s",
            "clear_quiz_attempt",
            deleted_count,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{deleted_count} old quiz attempt have been cleared."
            )
        )
