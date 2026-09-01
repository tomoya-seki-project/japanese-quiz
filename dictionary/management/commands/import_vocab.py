import logging
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

from django.db import IntegrityError

from getpass import getpass
import csv

from ...service.vocab_action import VocabActionService

from ...models import (
    VocabType,
    VocabLevel,
)
from ...models import (
    Vocab,
    VocabDetail,
    KatakanaDetail,
    Category,
)

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import vocab from a CSV file. Admin only."

    def add_arguments(self, parser):
        parser.add_argument("csv_file",type=str)

    def handle(self, *args, **options):
        username = input("Admin email: ")
        password = getpass("Admin password: ")

        user = authenticate(username=username, password=password)

        if user is None:
            raise CommandError("Login failed")

        if not user.is_superuser:
            raise CommandError("Admin account is required for this command")

        csv_file = options["csv_file"]
        self.stdout.write(csv_file)

        try:
            with open(csv_file, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                success_count = 0
                failed_rows = []

                required_headers = {
                    "word",
                    "kana",
                    "meaning",
                    "type",
                    "level",
                    "category1",
                    "category2",
                    "category3",
                    "native_japanese",
                }

                missing_headers = required_headers - set(reader.fieldnames or [])

                if missing_headers:
                    logger.warning(
                        "Vocab import rejected because CSV headers are missing: "
                        "operation=%s missing_headers=%s",
                        "vocab_import",
                        missing_headers,
                    )
                    raise CommandError(
                        f"Missing CSV headers: {', '.join(sorted(missing_headers))}"
                    )
                logger.info(
                    "Vocab import started: "
                    "operation=%s user_id=%s csv_file=%s",
                    "vocab_import",
                    user.pk,
                    csv_file,
                )
                for row_number, data in enumerate(reader, start=2):
                    if data["type"] != VocabType.VOCAB and data["type"] != VocabType.KATAKANA:
                        logger.warning(
                            "Vocab import row rejected: "
                            "operation=%s row_number=%s reason=%s",
                            "vocab_import",
                            row_number,
                            "vocab type unsupported",
                        )

                        failed_rows.append(
                            (row_number, "vocab type unsupported")
                        )
                        self.stderr.write(
                            self.style.ERROR(
                                f"Row {row_number}: vocab type unsupported."
                            )
                        )
                        continue
                    try:
                        category_names = [
                            data["category1"],
                            data["category2"] if data["category2"] != "---" else None,
                            data["category3"] if data["category3"] != "---" else None,
                        ]

                        category_names = [
                            name.strip()
                            for name in category_names
                            if name and name.strip()
                        ]

                        categories = Category.objects.filter(
                            name__in=category_names
                        )

                        found_names = set(
                            categories.values_list("name", flat=True)
                        )

                        missing_names = set(category_names) - found_names
                        if missing_names:
                            raise ValidationError(
                                f"These categories do not exist: {', '.join(missing_names)}"
                            )
                        VocabActionService.create_vocab(
                            {
                                "word": data["word"],
                                "kana": data["kana"],
                                "meaning": data["meaning"],
                                "type": data["type"],
                                "level": data["level"],
                                "categories": categories,
                                "native_japanese": data["native_japanese"],
                                "created_by": user,
                            },
                            approved_by=user
                        )
                        success_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Row {row_number}: imported {data['word']}:{data['kana']}"
                            )
                        )
                    except IntegrityError as e:
                        failed_rows.append(
                            (row_number, "Database integrity error.")
                        )
                        logger.warning(
                            "Vocab import row rejected due to a database integrity error: "
                            "operation=%s row_number=%s",
                            "vocab_import",
                            row_number,
                        )
                        self.stderr.write(
                            self.style.ERROR(
                                f"Row {row_number}: Database integrity error."
                            )
                        )
                        continue
                    except ValidationError as e:
                        error_message = "; ".join(e.messages)
                        failed_rows.append(
                            (row_number, error_message)
                        )
                        logger.warning(
                            "Vocab import row rejected: "
                            "operation=%s row_number=%s error=%s",
                            "vocab_import",
                            row_number,
                            error_message,
                        )
                        self.stderr.write(
                            self.style.ERROR(
                                f"Row {row_number}: {error_message}"
                            )
                        )
                        continue

                self.stdout.write("")
                self.stdout.write(self.style.SUCCESS(f"Imported rows: {success_count}"))
                self.stdout.write(self.style.WARNING(f"Failed rows: {len(failed_rows)}"))
                logger.info(
                    "Vocab import completed: "
                    "operation=%s success_count=%s failed_rows_count=%s",
                    "vocab_import",
                    success_count,
                    len(failed_rows),
                )
                for row_number, error_message in failed_rows:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Failed row {row_number}: {error_message}"
                        )
                    )
        except FileNotFoundError as e:
            logger.warning(
                "Vocab import failed because the CSV file was not found: "
                "operation=%s user_id=%s csv_file_path=%s",
                "vocab_import",
                user.pk,
                csv_file,
            )
            raise CommandError(f"CSV file not found: {csv_file}") from e
        except CommandError:
            raise
        except Exception:
            logger.exception(
                "Vocab import failed unexpectedly: "
                "operation=%s user_id=%s csv_file=%s",
                "vocab_import",
                user.pk,
                csv_file,
            )
            raise
