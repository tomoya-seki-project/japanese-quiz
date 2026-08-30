import logging
import csv
from django.core.management.base import BaseCommand, CommandError

from ...models import Category

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Set up basic categories from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        self.stdout.write(csv_file)

        try:
            with open(csv_file, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                success_count = 0
                failed_rows = []

                required_headers = {
                    "category",
                    "display",
                }

                missing_headers = required_headers - set(reader.fieldnames or [])

                if missing_headers:
                    logger.warning(
                        "Category setup rejected because CSV headers are missing: "
                        "operation=%s missing_headers=%s",
                        "setup_categories",
                        missing_headers,
                    )
                    raise CommandError(
                        f"Missing CSV headers: {', '.join(sorted(missing_headers))}"
                    )

                logger.info(
                    "Category setup started: "
                    "operation=%s csv_file=%s",
                    "setup_categories",
                    csv_file,
                )
                for row_number, data in enumerate(reader, start=2):
                    category_name = data["category"].strip()
                    display = data["display"].strip()

                    if not category_name:
                        failed_rows.append((row_number, "Category is required."))
                        self.stderr.write(
                            self.style.ERROR(
                                f"Row {row_number}: Category is required."
                            )
                        )
                        logger.warning(
                            "Category setup row rejected: "
                            "operation=%s row_number=%s error=%s",
                            "setup_categories",
                            row_number,
                            "Category is required.",
                        )
                        continue
                    category, created = Category.objects.update_or_create(
                        name=category_name,
                        defaults={
                            "display": display,
                        },
                    )
                    success_count += 1

                    action = "created" if created else "updated"
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Row {row_number}: {action} {category.name}:{category.display}"
                        )
                    )

                self.stdout.write("")
                self.stdout.write(self.style.SUCCESS(f"Imported rows: {success_count}"))
                self.stdout.write(self.style.WARNING(f"Failed rows: {len(failed_rows)}"))
                logger.info(
                    "Category setup completed: "
                    "operation=%s success_count=%s failed_rows_count=%s",
                    "setup_categories",
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
                "Category setup failed because the CSV file was not found: "
                "operation=%s csv_file_path=%s",
                "setup_categories",
                csv_file,
            )
            raise CommandError(f"CSV file not found: {csv_file}") from e
        except CommandError:
            raise
        except Exception:
            logger.exception(
                "Category setup failed unexpectedly: "
                "operation=%s csv_file=%s",
                "setup_categories",
                csv_file,
            )
            raise
