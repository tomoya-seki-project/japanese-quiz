from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

from django.db import IntegrityError

from getpass import getpass
import csv

from ...service.vocab_action import VocabActionService

from ...models import (
    VocabType,
    VocabCategory,
    VocabLevel,
)
from ...models import (
    Vocab,
    VocabDetail,
    KatakanaDetail,
)

class Command(BaseCommand):
    help = "Import vocab form CSV. for Admin only"

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
                    raise CommandError(
                        f"Missing CSV headers: {', '.join(sorted(missing_headers))}"
                    )

                for row_number, data in enumerate(reader, start=2):
                    try:
                        VocabActionService.create_vocab(
                            {
                                "word": data["word"],
                                "kana": data["kana"],
                                "meaning": data["meaning"],
                                "type": data["type"],
                                "level": data["level"],
                                "category": data["category1"],
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
                            (row_number, "database integrity error")
                        )
                        self.stderr.write(
                            self.style.ERROR(
                                f"Row {row_number}: database integrity error"
                            )
                        )
                        continue
                    except ValidationError as e:
                        error_message = "; ".join(e.messages)
                        failed_rows.append(
                            (row_number, error_message)
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
                for row_number, error_message in failed_rows:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Failed row {row_number}: {error_message}"
                        )
                    )
        except FileNotFoundError as e:
            raise CommandError(f"CSV file not found: {csv_file}")
