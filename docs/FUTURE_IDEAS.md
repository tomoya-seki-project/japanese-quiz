# Future Ideas

This document stores possible future directions that are not committed to the current development scope. When an idea becomes active work, it should move to `TODO.md` with an appropriate status.

## Contents

- [Accounts](#accounts)
- [Event Notifications](#event-notifications)
- [User Messages and Admin Inbox](#user-messages-and-admin-inbox)
- [Quiz](#quiz)
- [Scheduled Maintenance](#scheduled-maintenance)
- [Post-v1.0.0 Multiple-Choice Quiz](#post-v100-multiple-choice-quiz)
- [Vocabulary Data Model](#vocabulary-data-model)
- [Database Export and Restore](#database-export-and-restore)
- [CSV Import and Logging](#csv-import-and-logging)

## Accounts

- Add a password-reset flow using Django's built-in views, forms, and `default_token_generator`. Use a separate timeout policy if activation and password reset later require different expiry periods.
- Add quiz streak statistics to the user profile: longest correct streak, longest incorrect streak, and the current correct or incorrect streak. Decide during implementation whether to store separate counters or a streak type with one current count.

## Event Notifications

- Extend site announcements with publication time, expiry time, importance, active state, and target user groups.
- Include a reviewer reason or a more detailed result message in vocabulary-request result events.

## User Messages and Admin Inbox

- Preserve the relationship between a user message and its latest import batch so processing results remain traceable.
- If several users request vocabulary from the same import batch, notify every affected user of the result.

## Quiz

- Add the complete katakana answer flow.
- Implement a smartphone-style Japanese flick keyboard. Each key represents a kana row such as あ, か, さ, た, な, は, ま, や, or ら; holding and flicking selects another kana in that row.
- If recent-skip behaviour later needs greater precision, retain only the latest ten vocabulary IDs instead of introducing a complete question-history model.

## Scheduled Maintenance

- After v1.0.0, consider periodically increasing overdue `UserVocab.weight` according to `last_quiz_at`, stage-specific waiting periods, boost size, an upper bound, and the user's average weight.
- Define a retention policy and cleanup management command for completed, expired, and long-pending `QuizAttempt` records.
- Keep weight adjustment and attempt cleanup as separate commands so they can run at different frequencies and report failures independently. Both should support logging, processed counts, and `--dry-run`.
- Choose cron or the hosting platform's scheduler at deployment time. Do not introduce Celery Beat solely for these jobs unless the project later needs queues, retries, workers, or substantially more background processing.

## Post-v1.0.0 Multiple-Choice Quiz

- Re-enable `adverb`, `mimetic`, `conjunction`, and `colloquial` only after their complete question, option-generation, submission, checking, response, and rendering flow is implemented.
- Treat these values as project-specific learning categories rather than strict linguistic parts of speech. Resolve overlap in the order: inherent mimetic use, sentence-connecting role, modifier role, and finally colloquial recognition value. Send unresolved cases to an ambiguity queue with evidence instead of forcing a classification.
- Extend the CSV contract with `question1`, `question2`, `mc_answer1`, `mc_answer2`, and `mc_answer3` after `native_japanese`. Non-MC rows should use `---` for these fields.
- Give each sense two short, natural example questions. Hide the target with `____`, place inflection hints immediately after it, and normally limit each question to 50 Unicode characters, allowing up to 100 only when clarity requires it.
- Store the correct base form and three unique distractors. Every distractor must be clearly wrong for both questions and backed by verified natural usage.
- Validate blanks, literal `\n`, hints, length, grammar, inflection, semantics, and type. Randomise displayed options while preserving stable CSV roles.
- Keep one `Vocab` per `(word, kana)` and multiple `MCSense` records. Senses have independent meanings, questions, and distractors while sharing `UserVocab` learning state.
- Enforce `sense_no >= 1`, define a stable `sense_key`, and use `(vocab, sense_no)` as the within-vocabulary duplicate guard.
- Decide whether type, level, and categories must remain consistent across senses or whether some data belongs on `MCSense`.
- Extend import, services, admin, requests, detail pages, and answer checking as one vertical slice. Conflicts must produce an explicit report rather than silent success.
- Existing monthly CSV files are test data and should not be automatically deleted, overwritten, or upgraded.
- Restore public MC choices only after end-to-end tests cover import, review, administration, quiz, and result rendering.

## Vocabulary Data Model

- Add `Vocab.word_slug` after v1.0.0. Define its source fields, duplicate policy, update behaviour, and migration/backfill strategy first.

## Database Export and Restore

- After v1.0.0, consider `python manage.py export_whole <output_folder>` with separate model files, preserved keys and relationships, a manifest, and an explicit sensitive-data policy.
- Design the matching restore process around dependency order, schema/version preflight, dry-run support, and a single documented export contract.

## CSV Import and Logging

- Consider a database import-history model.
- Allow an admin-inbox/import report to update the originating user message with processing results.
- Duplicate rows currently produce terminal messages and logs. A future enhancement may export all duplicate rows to a separate CSV for review.

