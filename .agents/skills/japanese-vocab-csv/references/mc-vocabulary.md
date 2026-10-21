# Multiple-choice vocabulary rules

Read this file only when at least one candidate is classified as `adverb`,
`mimetic`, `conjunction`, or `colloquial`.

## Row semantics

Each MC row represents one meaning of one vocabulary item. Put the supplied
Japanese surface form in `word`, its reading entirely in hiragana in `kana`,
and `---` in `native_japanese`.

Use the matching category in `category1` for `adverb`, `mimetic`, and
`conjunction`. `colloquial` has no same-named category, so choose 1-3 existing
topic categories without inventing one.

When the user selects multiple senses, create one row per sense. Each row's
`meaning`, both questions, and all distractors must test only that sense. The
same `(word, kana)` may appear in several MC rows when the meanings differ;
never duplicate the same type and meaning.

## Questions

Generate two short, natural Japanese usage prompts in `question1` and
`question2`:

- use a single sentence when dialogue adds no value;
- use `Q：...\nA：...` only when dialogue is natural;
- store `\n` as the two literal characters backslash and `n`, never an actual
  newline;
- replace the target occurrence with exactly four ASCII underscores, `____`;
- include exactly one target blank and do not reveal the answer elsewhere;
- keep each stored question at or below 50 Unicode characters when practical;
  use 51-100 only when needed for natural context or disambiguation, and never
  exceed 100.

Both prompts must test only the row's intended meaning. Rewrite a prompt if a
distractor would also be a defensible answer.

### Inflected answers

Keep `word` and all choices in dictionary/basic form. When the completed
sentence needs inflection, add a concise ASCII cue immediately after the blank,
such as `____(て)`, `____(ない)`, `____(され)`, `____(られ)`, or
`____(させ)`.

The cue must not mechanically reveal the correct option. Prefer distractors
that can take the same required inflection in both prompts.

## Distractors

Store three real Japanese basic forms:

- `mc_answer1`: semantically close or easily confused, but incorrect in both
  questions;
- `mc_answer2`: the exact same project type as `word`, but clearly incorrect
  in both questions;
- `mc_answer3`: any MC project type, possibly different from `word`, but
  clearly incorrect in both questions.

The correct `word` and all three distractors must be distinct. Validate every
distractor against both questions for meaning, syntax, and inflection. Prefer
meaning-based difficulty; do not use an option that can be eliminated solely
because its part of speech or conjugation is incompatible.

Distractors need not already exist in repository CSVs or the database, but they
must be verified real, natural words or expressions. They are option text, not
foreign keys.

## Sense-specific checks

Before handing rows to the helper, confirm that:

- both prompts test the same meaning recorded in that row;
- no prompt hints at or depends on another selected sense;
- every blank and optional inflection cue follows the storage contract;
- every distractor is wrong in both prompts;
- `mc_answer1` remains plausibly confusing;
- `mc_answer2` has the same project type;
- `mc_answer3` belongs to an MC type;
- all four choices are distinct basic forms.

These semantic checks require language judgment. The helper performs the
mechanical schema, length, placeholder, category, blank-count, and exact-row
duplicate checks.
