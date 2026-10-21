---
name: japanese-vocab-csv
description: Research and append Japanese words, including staged multiple-choice vocabulary, to this repository's monthly 14-column CSV. Use when the user clearly asks to add, save, collect, or record vocabulary; do not use for explanation or comparison alone.
---

# Japanese Vocabulary CSV

Turn user-supplied words into researched, import-ready or staged rows under
`resource/`. The CSV is the collection boundary: `vocab` and `katakana` can be
imported now, while multiple-choice rows remain valid staged data until the
repository importer supports them.

## Resolve the repository

Resolve the active Git root with `git rev-parse --show-toplevel`; never reuse a
remembered path or another clone. Before writing, verify that the root contains
this skill, `AGENTS.md`, `resource/categories.csv`, `dictionary/models.py`, and
`dictionary/management/commands/import_vocab.py`. If the user's intended clone
and the active root differ, stop and ask which writable clone to use.

Use [`scripts/manage_vocab_csv.py`](scripts/manage_vocab_csv.py) for repository
context, deterministic validation, duplicate checks, and writes. Do not edit a
monthly CSV manually.

## Trigger boundary

Collection intent includes natural requests to add, save, collect, record, or
remember one or more words. A request only for meaning, reading, origin, usage,
or comparison is not permission to write. At a natural stopping point, ask
once whether a discussed word should be recorded; no answer means no write.

## Workflow

1. Run the helper's `context` command. Use its current category list,
   destination, header state, and supported/staged type information instead of
   reproducing those facts in the prompt.
2. Classify every candidate by its intended quiz interaction and sense. The six
   project types are described below.
3. If any candidate is an MC type, read
   [`references/mc-vocabulary.md`](references/mc-vocabulary.md) completely
   before enriching that candidate. Do not read it for a request containing
   only `vocab` and `katakana`.
4. Research the intended sense, reading or source-language origin, and JLPT
   estimate. Batch independent lookups where practical.
5. Hold unresolved candidates out of the write, but continue with clear words.
6. Put the completed candidates in a temporary JSON array using the exact
   14-field schema emitted by `context`.
7. Run `validate`, correct any reported error, then run `append` with the same
   JSON file. Do not append a candidate that fails validation.
8. Build the final response from the helper's persisted-row output.

Example commands, run from the resolved repository root:

```bash
python3 .agents/skills/japanese-vocab-csv/scripts/manage_vocab_csv.py context
python3 .agents/skills/japanese-vocab-csv/scripts/manage_vocab_csv.py validate --rows /tmp/vocab-rows.json
python3 .agents/skills/japanese-vocab-csv/scripts/manage_vocab_csv.py append --rows /tmp/vocab-rows.json
```

## Project type classification

Classify by the intended learning interaction when that differs from a general
dictionary part-of-speech label:

- `vocab`: ordinary kanji or hiragana vocabulary tested by producing its kana.
- `katakana`: a conventional katakana form tested from its source-language
  term; the row also stores a native-Japanese equivalent.
- `mimetic`: inherently sound-symbolic or mimetic language.
- `conjunction`: primarily connects clauses or discourse.
- `adverb`: primarily modifies an action, state, degree, or proposition.
- `colloquial`: slang, contractions, internet coinages, informal fixed
  expressions, or recognition-oriented project cases not better represented by
  the first three MC types.

For plausible overlap among MC types, prefer `mimetic`, then `conjunction`,
then `adverb`, then `colloquial`, based on the intended sense rather than
spelling alone. Do not label every casual-sounding word `colloquial`.

The current importer accepts only `vocab` and `katakana`; this is not a reason
to discard MC candidates. Append complete MC rows to the monthly CSV. The
importer may filter them until database support is enabled.

## Resolve ambiguity

Use the user's context to select the intended sense. Ask only when the choice
would materially change the reading, source term, type, meaning, or row
identity. For each unresolved word, show only the common supported senses, at
most three, with a short meaning, proposed project type, and source. Let the
user choose one, several, or none.

Treat each selected MC sense as its own row with sense-specific meaning,
questions, and distractors. The staging CSV may therefore contain the same
`word` and `kana` for distinct MC meanings; the helper rejects an exact repeated
MC sense rather than rejecting all such rows. `vocab` and `katakana` continue to
follow the repository's `(word, kana)` uniqueness rule.

## Research and enrichment

Use web research for reading, intended sense, origin where relevant, and JLPT
estimate. Prefer Japanese dictionaries or primary lexical sources. JLPT does
not publish a fixed official vocabulary list, so describe levels as estimates.

For every row:

- `level` is `0`-`5`; use `0` when evidence cannot support N1-N5. When credible
  estimates disagree, choose the easier/lower-proficiency level, such as `3`
  for an N2/N3 disagreement.
- `meaning` is a short, simple Japanese explanation of only the intended sense.
- choose 1-3 distinct current categories, strongest first; never invent one.
- preserve the user's candidate order, apart from unresolved or invalid rows
  that must be held back.

For `vocab`:

- use the Japanese surface form in `word`;
- put the standard reading entirely in hiragana in `kana`;
- set `native_japanese` and all five MC fields to `---`.

For `katakana`:

- put the established Latin-script source term in `word`;
- preserve the conventional katakana answer in `kana`;
- put a concise native-Japanese equivalent in `native_japanese`;
- set all five MC fields to `---`;
- ask when the intended sense changes the source term, such as `リスト` meaning
  “list” versus “wrist”.

For an MC type, follow the conditional MC reference. Put the user-supplied
Japanese form in `word`, its reading entirely in hiragana in `kana`, and `---`
in `native_japanese`.

## CSV and duplicate rules

The helper owns the monthly destination, exact 14-column header, quoting,
allowed categories, placeholders, field lengths, duplicate scan, and append.
Treat existing 14-column monthly files as staged collection data, including MC
rows; do not delete, overwrite, or dismiss them as disposable.

If the destination has an incompatible header, stop and report it. Do not
migrate or replace it without a separate user request. Repository models and
the importer remain authoritative when the implemented schema changes; update
the helper and this skill together rather than silently coercing old data.

## Final response

Link the destination CSV and show each persisted row in a readable form.

- For `vocab` and `katakana`, show `word`, `kana`, `type`, `level`, `meaning`,
  categories, and `native_japanese`; state once that MC fields were validated
  as `---` instead of printing five placeholder columns per row.
- For MC rows, also show both questions and all three distractors.
- Briefly give the intended sense, reading or origin, JLPT evidence and chosen
  level, with citations close to the claims.
- List duplicates, invalid candidates, and unresolved words that were not
  appended, with the reason.

Keep the report concise when sources agree; never report planned values as if
they were persisted.
