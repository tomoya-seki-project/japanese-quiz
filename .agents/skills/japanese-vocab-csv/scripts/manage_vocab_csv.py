#!/usr/bin/env python3
"""Validate and append Japanese Quiz vocabulary staging rows."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


FIELDS = [
    "word",
    "kana",
    "type",
    "level",
    "meaning",
    "category1",
    "category2",
    "category3",
    "native_japanese",
    "question1",
    "question2",
    "mc_answer1",
    "mc_answer2",
    "mc_answer3",
]
COLLECTION_TYPES = {
    "vocab",
    "katakana",
    "adverb",
    "mimetic",
    "conjunction",
    "colloquial",
}
IMPORTABLE_TYPES = {"vocab", "katakana"}
MC_TYPES = {"adverb", "mimetic", "conjunction", "colloquial"}
MATCHING_CATEGORY_TYPES = {"adverb", "mimetic", "conjunction"}
PLACEHOLDER = "---"
MC_FIELDS = ["question1", "question2", "mc_answer1", "mc_answer2", "mc_answer3"]
REQUIRED_REPOSITORY_PATHS = [
    "AGENTS.md",
    ".agents/skills/japanese-vocab-csv/SKILL.md",
    "resource/categories.csv",
    "dictionary/models.py",
    "dictionary/management/commands/import_vocab.py",
]


class ValidationFailure(Exception):
    """Raised for user-correctable candidate or repository errors."""


def emit(payload: dict[str, Any]) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def resolve_root(explicit_root: str | None) -> Path:
    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
    else:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
        root = Path(result.stdout.strip()).resolve()

    missing = [relative for relative in REQUIRED_REPOSITORY_PATHS if not (root / relative).is_file()]
    if missing:
        raise ValidationFailure(
            f"Not a Japanese Quiz repository root ({root}); missing: {', '.join(missing)}"
        )
    return root


def destination_for(root: Path) -> Path:
    month = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y_%m")
    return root / "resource" / f"NewWord_{month}.csv"


def read_header(path: Path) -> list[str] | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle), None)


def read_categories(root: Path) -> list[str]:
    path = root / "resource" / "categories.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "category" not in reader.fieldnames:
            raise ValidationFailure(f"{path} has no 'category' column")
        categories = [row["category"].strip() for row in reader if row.get("category", "").strip()]
    if not categories:
        raise ValidationFailure(f"{path} contains no categories")
    return categories


def load_candidate_rows(path: Path) -> list[dict[str, str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"Cannot read candidate JSON {path}: {exc}") from exc

    if not isinstance(raw, list) or not raw:
        raise ValidationFailure("Candidate JSON must be a non-empty array")

    rows: list[dict[str, str]] = []
    expected = set(FIELDS)
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValidationFailure(f"Row {index}: expected an object")
        actual = set(item)
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing or extra:
            details = []
            if missing:
                details.append(f"missing {missing}")
            if extra:
                details.append(f"unexpected {extra}")
            raise ValidationFailure(f"Row {index}: {'; '.join(details)}")
        if any(not isinstance(item[field], str) for field in FIELDS):
            raise ValidationFailure(f"Row {index}: all field values must be strings")
        rows.append({field: item[field].strip() for field in FIELDS})
    return rows


def vocabulary_csv_paths(root: Path) -> list[Path]:
    return sorted(
        path
        for path in (root / "resource").glob("*.csv")
        if path.name != "categories.csv"
    )


def read_existing_rows(root: Path) -> list[tuple[Path, int, dict[str, str]]]:
    rows: list[tuple[Path, int, dict[str, str]]] = []
    for path in vocabulary_csv_paths(root):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or not {"word", "kana"}.issubset(reader.fieldnames):
                continue
            for line_number, row in enumerate(reader, start=2):
                if row.get("word") and row.get("kana"):
                    rows.append((path, line_number, row))
    return rows


def validate_row(index: int, row: dict[str, str], categories: set[str]) -> list[str]:
    errors: list[str] = []
    prefix = f"Row {index}"

    for field in FIELDS:
        if not row[field]:
            errors.append(f"{prefix}: {field} is empty; use '{PLACEHOLDER}' only where allowed")

    row_type = row["type"]
    if row_type not in COLLECTION_TYPES:
        errors.append(f"{prefix}: unsupported type '{row_type}'")
    if row["level"] not in {"0", "1", "2", "3", "4", "5"}:
        errors.append(f"{prefix}: level must be 0-5")

    limits = {
        "word": 50,
        "kana": 255,
        "meaning": 255,
        "native_japanese": 255,
        "mc_answer1": 20,
        "mc_answer2": 20,
        "mc_answer3": 20,
    }
    for field, limit in limits.items():
        if row[field] != PLACEHOLDER and len(row[field]) > limit:
            errors.append(f"{prefix}: {field} exceeds {limit} characters")

    selected_categories = [
        row[field] for field in ("category1", "category2", "category3") if row[field] != PLACEHOLDER
    ]
    if not selected_categories:
        errors.append(f"{prefix}: at least category1 is required")
    if row["category1"] == PLACEHOLDER:
        errors.append(f"{prefix}: category1 cannot be a placeholder")
    if len(selected_categories) != len(set(selected_categories)):
        errors.append(f"{prefix}: categories must be distinct")
    unknown = sorted(set(selected_categories) - categories)
    if unknown:
        errors.append(f"{prefix}: unknown categories {unknown}")
    if row_type in MATCHING_CATEGORY_TYPES and row["category1"] != row_type:
        errors.append(f"{prefix}: {row_type} requires category1={row_type}")

    if row_type == "katakana":
        if row["native_japanese"] == PLACEHOLDER:
            errors.append(f"{prefix}: katakana requires native_japanese")
    elif row["native_japanese"] != PLACEHOLDER:
        errors.append(f"{prefix}: only katakana may set native_japanese")

    if row_type in IMPORTABLE_TYPES:
        for field in MC_FIELDS:
            if row[field] != PLACEHOLDER:
                errors.append(f"{prefix}: {row_type} requires {field}={PLACEHOLDER}")
    elif row_type in MC_TYPES:
        for field in MC_FIELDS:
            if row[field] == PLACEHOLDER:
                errors.append(f"{prefix}: MC type requires {field}")
        for field in ("question1", "question2"):
            question = row[field]
            if "\n" in question:
                errors.append(f"{prefix}: {field} contains an actual newline; store literal \\n")
            if len(question) > 100:
                errors.append(f"{prefix}: {field} exceeds 100 characters")
            if question.count("____") != 1:
                errors.append(f"{prefix}: {field} must contain exactly one ____ blank")
        choices = [row["word"], row["mc_answer1"], row["mc_answer2"], row["mc_answer3"]]
        if len(choices) != len(set(choices)):
            errors.append(f"{prefix}: word and MC distractors must be distinct")

    return errors


def duplicate_errors(
    candidates: list[dict[str, str]],
    existing: list[tuple[Path, int, dict[str, str]]],
) -> list[str]:
    errors: list[str] = []
    standard_ids: dict[tuple[str, str], str] = {}
    mc_ids: dict[tuple[str, str, str, str], str] = {}

    for path, line_number, row in existing:
        row_type = row.get("type", "")
        location = f"{path.name}:{line_number}"
        if row_type in MC_TYPES:
            key = (row.get("word", ""), row.get("kana", ""), row_type, row.get("meaning", ""))
            mc_ids.setdefault(key, location)
        else:
            standard_ids.setdefault((row.get("word", ""), row.get("kana", "")), location)

    for index, row in enumerate(candidates, start=1):
        if row["type"] in MC_TYPES:
            key = (row["word"], row["kana"], row["type"], row["meaning"])
            if key in mc_ids:
                errors.append(f"Row {index}: duplicate MC sense already at {mc_ids[key]}")
            else:
                mc_ids[key] = f"candidate row {index}"
        else:
            key = (row["word"], row["kana"])
            if key in standard_ids:
                errors.append(f"Row {index}: duplicate (word, kana) already at {standard_ids[key]}")
            else:
                standard_ids[key] = f"candidate row {index}"
    return errors


def validate_candidates(
    root: Path, candidates: list[dict[str, str]]
) -> tuple[list[str], list[str]]:
    destination = destination_for(root)
    header = read_header(destination)
    errors: list[str] = []
    warnings: list[str] = []

    if header is not None and header != FIELDS:
        errors.append(
            f"{destination}: incompatible header; expected {FIELDS}, found {header}"
        )

    categories = set(read_categories(root))
    for index, row in enumerate(candidates, start=1):
        errors.extend(validate_row(index, row, categories))
        if row["type"] in MC_TYPES:
            warnings.append(
                f"Row {index}: {row['type']} is staged; the current importer filters this type"
            )
    errors.extend(duplicate_errors(candidates, read_existing_rows(root)))
    return errors, warnings


def append_rows(root: Path, rows: list[dict[str, str]]) -> list[dict[str, str]]:
    destination = destination_for(root)
    exists = destination.exists()
    with destination.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)

    with destination.open(encoding="utf-8-sig", newline="") as handle:
        persisted = list(csv.DictReader(handle))[-len(rows):]
    if persisted != rows:
        raise ValidationFailure("Persisted rows did not match the validated candidates")
    return persisted


def context_payload(root: Path) -> dict[str, Any]:
    destination = destination_for(root)
    header = read_header(destination)
    if header is None:
        header_state = "missing_will_create"
    elif header == FIELDS:
        header_state = "compatible"
    else:
        header_state = "incompatible"

    return {
        "status": "ok",
        "repository_root": str(root),
        "destination": str(destination),
        "destination_header": header_state,
        "fields": FIELDS,
        "categories": read_categories(root),
        "collection_types": sorted(COLLECTION_TYPES),
        "currently_importable_types": sorted(IMPORTABLE_TYPES),
        "staged_types": sorted(MC_TYPES),
        "existing_vocabulary_rows": len(read_existing_rows(root)),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", help="Explicit Japanese Quiz repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("context", help="Print current deterministic CSV context")
    for command in ("validate", "append"):
        child = subparsers.add_parser(command)
        child.add_argument("--rows", required=True, type=Path, help="Candidate JSON array")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        root = resolve_root(args.repo_root)
        if args.command == "context":
            emit(context_payload(root))
            return 0

        rows = load_candidate_rows(args.rows)
        errors, warnings = validate_candidates(root, rows)
        if errors:
            emit({"status": "invalid", "errors": errors, "warnings": warnings})
            return 2
        if args.command == "validate":
            emit(
                {
                    "status": "valid",
                    "destination": str(destination_for(root)),
                    "row_count": len(rows),
                    "warnings": warnings,
                }
            )
            return 0

        persisted = append_rows(root, rows)
        emit(
            {
                "status": "appended",
                "destination": str(destination_for(root)),
                "row_count": len(persisted),
                "persisted_rows": persisted,
                "warnings": warnings,
            }
        )
        return 0
    except (ValidationFailure, subprocess.CalledProcessError) as exc:
        emit({"status": "error", "error": str(exc)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
