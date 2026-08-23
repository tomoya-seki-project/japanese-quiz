---
name: japanese-vocab-csv
description: Research and append new Japanese words to this repository's monthly import CSV. Use when the user expresses a clear intent to add, save, collect, or record Japanese vocabulary in natural language; enrich each word with its quiz answer, an estimated JLPT level, a short Japanese meaning, and 1-3 existing categories. Do not use for a vocabulary question or comparison without collection intent.
---

# Japanese Vocabulary CSV

Turn words supplied by the user into import-ready rows under `resource/` without
making them request each enrichment step separately.

## Repository root resolution

Before reading or writing project files, resolve the active workspace's Git
root with `git rev-parse --show-toplevel`. Treat `.agents/`, `resource/`,
`dictionary/`, and every other repository path as relative to that root; never
reuse an absolute path or working directory remembered from an earlier turn or
another clone.

Verify that the resolved root contains this repository's `AGENTS.md`, this
skill, `resource/categories.csv`, and the relevant model/import files before
writing. A skill locator may identify another installed or cloned copy but must
not silently redirect CSV output there. If the user identifies a different
clone or the active tool workspace and intended editor workspace disagree,
stop all writes, report both canonical paths, and continue only after the target
workspace has been confirmed and is writable.

## Trigger boundary

Do not require a fixed command such as `有新字:`. Treat natural phrases showing
clear collection intent as equivalent, including requests to add, save, record,
collect, or remember words and statements such as having newly learned words
when the context indicates they should enter the collection.

A request that only asks for a meaning, reading, origin, usage explanation, or
comparison is not permission to modify the CSV. Answer that request normally.
If the discussion produces a plausible word for the collection, ask once at a
natural stopping point whether the user wants it recorded. No answer means do
not write it, and do not repeatedly ask during the same discussion.

## Repository sources

Before processing words, read:

- `resource/categories.csv` for the current allowed category names;
- the header and representative rows in an existing `resource/*.csv` vocabulary
  file;
- `dictionary/models.py` and
  `dictionary/management/commands/import_vocab.py` only when the schema or
  validation behavior is unclear or has changed.

Repository files are authoritative for the CSV schema and allowed values. Do
not copy the category list into this skill because the repository list may
change.

## Additional type rollout boundary

`VocabType` now declares four additional vocabulary types:

- `adverb`
- `mimetic`
- `conjunction`
- `colloquial`

Their enum presence is preparation only; these four types are not enabled for
new-word CSV collection yet. Classify each supplied word before enrichment. If
it belongs to `adverb`, `mimetic`, `conjunction`, or `colloquial`:

- skip that word completely;
- do not append it to any CSV;
- do not downgrade or relabel it as `vocab`;
- report the detected planned type and explain that collection for that type is
  not enabled yet.

Continue processing other supported `vocab` or `katakana` words from the same
request. Do not invent a `colloquial` category or output a partially implemented
type.

These types are project-specific quiz modes, not a pure linguistic taxonomy:

- `vocab` and `katakana` use a kana keyboard and test production of the answer;
- `adverb`, `mimetic`, `conjunction`, and `colloquial` are intended to use
  multiple-choice questions;
- classify by the intended learning interaction when that conflicts with a
  dictionary part-of-speech label.

When these four types are enabled for collection, put the Japanese surface form
supplied by the user in `word` and its reading entirely in hiragana in `kana`.
Set `native_japanese=---`; only `katakana` uses a non-placeholder value in that
field. Do not apply the katakana source-language question mapping to MC types.

For `type=adverb`, `type=mimetic`, and `type=conjunction`, put the matching
same-named category in `category1`. Choose any additional categories by topic.
`colloquial` currently has no same-named category, so choose 1-3 existing
categories by topic without inventing one.

Use `colloquial` for slang, contractions, internet coinages, informal
expressions, and items whose written form is more useful to recognize by
multiple choice than to reproduce with a kana keyboard. Under this project's
taxonomy, `ググる`, `あざっす`, and `ズレ` are `colloquial`. `ズレ` may be a
general noun linguistically, but it must not fall back to `vocab`, because asking
the learner to reproduce the same kana spelling is not the intended exercise.

Do not classify every casual-sounding word as `colloquial`. Prefer `adverb`,
`mimetic`, or `conjunction` when one of those is the intended multiple-choice
learning category; for example, classify `やっぱり` as `adverb`.

When a word plausibly matches multiple MC types, use this priority based on its
primary learning function:

1. `mimetic` when the word is inherently sound-symbolic or mimetic, even if it
   functions adverbially in a sentence;
2. `conjunction` when its primary role is connecting clauses or discourse;
3. `adverb` when its primary role is modifying an action, state, degree, or
   proposition;
4. `colloquial` for slang, contractions, internet coinages, informal fixed
   expressions, or the project-specific MC cases described above that are not
   better represented by the first three types.

If evidence and context still do not support one type confidently, use the
ambiguity queue instead of forcing the priority mechanically.

### Ambiguity queue

Use the user's surrounding context to identify the intended sense before
classifying it. This applies both to uncertainty between `colloquial` and
another type and to any word with multiple plausible senses. Do not infer type
from katakana spelling alone.

In a request containing both clear and ambiguous words:

1. Complete all clear words first.
2. Hold every ambiguous word out of the CSV.
3. At the end, group the unresolved words and show up to three common senses for
   each one, with a short meaning, proposed project type, and supporting source.
   Use frequency evidence when available; otherwise call them common senses,
   not a precise popularity ranking. Show only the common senses actually
   supported: one when there is one, two when there are two, and at most three.
   Never pad the list with a rare, obsolete, technical, or weakly supported
   sense merely to reach three choices.
4. Ask the user to choose one sense, multiple senses, or none.
5. After selection, treat every chosen sense as a separate candidate row with
   its own meaning, type, categories, questions, and distractors.

If the user selects multiple senses, create one row per selected sense. In each
row, both `question1` and `question2` must test only that row's `meaning`. Do not
mix, hint at, or rely on another selected sense in either question or its
distractors.

Do not write an ambiguous candidate before the user chooses. If multiple chosen
senses would conflict with the repository's current uniqueness rule, report
that constraint and wait until the schema supports separate sense rows.

For example:

- `ノリ` meaning atmosphere, momentum, or social energy may be `colloquial`,
  while `のり` meaning seaweed or glue is ordinary `vocab`;
- `ボケ` meaning the comedy role may be `colloquial`, while photographic blur
  or another ordinary noun sense may require a different classification.

Do not ask when the conversation already establishes one intended sense.

Before enabling an additional type here, inspect its implemented model, answer,
and import semantics; do not assume its field mapping matches either current
type.

## Research each word

Use web research for the reading, relevant sense, and JLPT estimate. Prefer
Japanese dictionary or other primary lexical sources for reading and meaning.
JLPT vocabulary levels are estimates because JLPT does not publish a fixed
official vocabulary list; do not describe an estimate as official.

For each word:

1. Identify the sense intended by the user's context. If materially ambiguous,
   ask a concise clarification instead of guessing. Clear words in a multi-word
   request may still be processed while ambiguous ones wait for clarification.
2. For ordinary vocabulary, put the standard reading entirely in hiragana in
   `kana`.
3. Set `level` to one of the strings `0`, `1`, `2`, `3`, `4`, or `5`.
   - Use `0` when available evidence cannot support an N1-N5 estimate.
   - When credible sources place a word at different levels, choose the lower
     proficiency/easier level. For example, an N2/N3 disagreement becomes `3`.
4. Write `meaning` as a short, simple Japanese explanation consistent with the
   style of existing rows. Explain the intended sense, not every dictionary
   sense.
5. Choose 1-3 distinct categories using only names currently present in
   `resource/categories.csv`. Put the strongest match first. Do not invent a
   category.
6. Use `type=vocab` for ordinary kanji or hiragana vocabulary and set
   `native_japanese=---`.
7. For katakana vocabulary, treat the katakana supplied by the user as the quiz
   answer rather than as the question:
   - Set `type=katakana`.
   - Research the original source-language term and put its Latin-script form
     in `word`, for example `スマホ` becomes `word=smartphone` and `リスト` in
     the “list” sense becomes `word=list`.
   - Preserve the conventional katakana form in `kana`, for example
     `kana=スマホ`; do not convert it to hiragana.
   - Put a concise native-Japanese equivalent in `native_japanese`, such as
     `携帯電話` or `一覧`. Do not use `---` for a katakana row because the
     application requires this field during approval.
   - Research JLPT level, meaning, and categories for the Japanese katakana
     word and its intended sense, not merely for the source-language spelling.
   - If the source term is disputed, abbreviated, or sense-dependent, use the
     established origin for that Japanese word. Ask for clarification when the
     user's intended sense changes the source term, such as `リスト` meaning
     English “list” versus “wrist”.

## Prevent duplicates

Before writing, inspect the repository's current model uniqueness rule and scan
vocabulary CSV files under `resource/` using that identity. Also deduplicate
within the current request. Do not append a row that violates the active rule.
Report skipped or schema-blocked candidates to the user.

Do not silently treat the same spelling with a different reading or meaning as
a duplicate; verify whether it is a distinct word or sense. While the model
still enforces `(word, kana)` uniqueness, do not write multiple sense rows with
the same pair. Once that rule changes, follow the implemented identity rather
than retaining the old pair-only assumption.

## Write the monthly CSV

Use the current year and month in Asia/Tokyo. The destination is:

```text
resource/NewWord_YYYY_MM.csv
```

Create it if missing, or append to it if present. Preserve the order in which
the user supplied multiple words.

Monthly CSVs managed by this skill use exactly this 14-column order:

```csv
word,kana,type,level,meaning,category1,category2,category3,native_japanese,question1,question2,mc_answer1,mc_answer2,mc_answer3
```

Use `---` for unused `category2` or `category3`. Use proper CSV quoting whenever
a value contains a comma, quote, or newline. Do not reorder older rows. For
`vocab` and `katakana`, set all five multiple-choice fields (`question1`,
`question2`, `mc_answer1`, `mc_answer2`, and `mc_answer3`) to `---`.

### Multiple-choice question fields

For each enabled multiple-choice word, generate two short, natural Japanese
usage prompts in `question1` and `question2`. They do not need to share one
format:

- use a single sentence when dialogue adds no value;
- use a `Q：...\nA：...` exchange only when question-and-answer context is
  natural;
- store `\n` as the two literal characters backslash and `n`, not as an actual
  newline;
- replace the target occurrence with exactly four ASCII underscores: `____`;
- include only one target blank per prompt and do not reveal the word elsewhere
  in that prompt.

Measure each stored question independently by Unicode characters, including
the literal `\n` as two characters, all four underscores, punctuation, and any
inflection cue. Aim for at most 50 characters. Use 51-100 characters only when
the extra context is necessary for natural Japanese or to eliminate another
defensible answer. Never exceed 100 characters in either question.

Both prompts must use only the exact sense represented by that row's `meaning`.
For a polysemous word stored in multiple rows, generate a separate pair of
sense-specific prompts for every row.

When the sentence requires an inflected form, keep the correct choice and
`word` in dictionary/basic form. Immediately after the blank, add a concise
inflection cue in ASCII parentheses, for example `____(て)`, `____(ない)`,
`____(され)`, `____(られ)`, or `____(させ)`. Do not put Markdown backticks in
the CSV. The completed sentence may therefore use `ググって`, while the stored
correct choice remains `ググる`:

```text
Q：分からない言葉はどうしますか？\nA：ネットで____(て)みます
```

The four choices consist of the correct basic form from `word` plus three
generated distractors, also stored in basic form:

- `mc_answer1`: a semantically close or easily confused word. It must still be
  incorrect in both `question1` and `question2`.
- `mc_answer2`: a word with the exact same project type as `word`, but clearly
  incorrect in both questions.
- `mc_answer3`: a word belonging to one of the four MC types (`adverb`,
  `mimetic`, `conjunction`, or `colloquial`). It may have a different type from
  `word`, but must be clearly incorrect in both questions.

All four choices must be distinct. Validate every distractor against both
questions, including the intended sense, syntax, and any inflection cue. A
semantically close distractor that can naturally complete either prompt is not
valid. Rewrite the ambiguous prompt or choose another distractor rather than
shipping a question with multiple defensible answers.

Make all three distractors grammatically compatible with the blank and its
inflection cue in both questions whenever reasonably possible. They should be
wrong because their meanings do not fit the context, not be trivially
eliminated from part of speech, conjugation, or sentence structure alone. If a
candidate exposes the answer mechanically, replace the candidate or rewrite
the prompt while preserving the row's intended sense.

Distractors do not need to exist as `Vocab` records or appear in repository CSV
files. Research or generate suitable choices from Japanese vocabulary outside
the current database when needed. Each distractor must still be a real, natural
Japanese word or expression with a verified meaning and project-type
classification; never invent a fake form merely to make an option incorrect.
Treat `mc_answer1`-`mc_answer3` as self-contained option text, not as implied
foreign keys to the vocabulary collection.

Do not enable CSV collection for `adverb`, `mimetic`, `conjunction`, or
`colloquial` until the repository flow can import, store, and use these fields.

Existing `NewWord_YYYY_MM.csv` files created during schema design are disposable
test artifacts and are not migration inputs. The user will delete them before
the 14-column workflow is enabled. Do not delete, overwrite, upgrade, or rely on
them. If a legacy same-month file still exists when a write is requested, stop
and report the conflict rather than replacing it. Do not bulk-migrate historical
resource CSVs unless the user separately asks.

## Validate before finishing

After writing, verify:

- the destination has the exact 14-column header;
- every row has exactly 14 fields;
- `type` is `vocab` or `katakana`;
- `level` is `0`-`5`;
- there are 1-3 non-placeholder, distinct, allowed categories;
- every non-katakana type uses `native_japanese=---`, while katakana vocabulary
  has a non-placeholder native-Japanese equivalent;
- `adverb`, `mimetic`, and `conjunction` use their matching type as `category1`;
- enabled MC questions follow the blank, literal `\n`, and inflection-cue
  contract above;
- each question is at most 100 Unicode characters and exceeds the 50-character
  target only for justified context or disambiguation;
- `word` and all three MC distractors are distinct basic forms;
- each distractor is incorrect in both questions, and `mc_answer1` remains
  meaningfully close enough to be a useful distractor;
- distractors are grammatically compatible with both blanks whenever
  reasonably possible and cannot be eliminated mechanically by the inflection
  cue or sentence structure alone;
- `mc_answer2` has the same project type as `word`, while `mc_answer3` belongs
  to one of the four MC types;
- distractors not present in the repository are verified as real Japanese words
  or expressions and do not require matching `Vocab` records;
- the write satisfies the repository's active uniqueness rule across resource
  vocabulary CSV files.

After validation, read the appended rows back from the destination CSV. Build
the final response from those persisted values rather than from the planned
rows, so the report cannot silently differ from the file.

## Report what was added

In the final response:

- name and link the destination CSV;
- show every newly appended row in a readable table with all 14 fields:
  `word`, `kana`, `type`, `level`, `meaning`, `category1`, `category2`,
  `category3`, `native_japanese`, `question1`, `question2`, `mc_answer1`,
  `mc_answer2`, and `mc_answer3`;
- for each word, briefly show the researched reading or source-language origin,
  intended sense, JLPT evidence and resulting level, including disagreements or
  why `0` was used;
- cite the dictionary and JLPT research sources close to the claims they
  support;
- list duplicates or unresolved words that were skipped, with the reason.

Do not replace this report with only a count or a generic success message. Keep
the explanation concise when the research sources agree.
